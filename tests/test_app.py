from fast_zero.schemas import UserPublic


def test_root_deve_retornar_200_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == 200
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'carlos',
            'email': 'carlos@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        'username': 'carlos',
        'email': 'carlos@example.com',
        'id': 1,
    }


def test_create_user_exception_already_registered(client):

    test_create_user(client)

    response = client.post(
        '/users/',
        json={
            'username': 'carlos',
            'email': 'carlos@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Email already registered'}


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == 200
    assert response.json() == {'users': []}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


# def test_update_user_exception_not_found(client, user):
#     response = client.put(
#         '/users/0',
#         json={
#             'username': 'alison',
#             'email': 'alison@hotmail.com',
#             'password': 'mynewpassword',
#         },
#     )
#     assert response.status_code == 404
#     assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 200
    assert response.json() == {'detail': 'User deleted'}


# def test_delete_user_exception_not_found(client, user):
#     response = client.delete('/users/0')
#     assert response.status_code == 404
#     assert response.json() == {'detail': 'User not found'}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == 200
    assert 'access_token' in token
    assert 'token_type' in token
