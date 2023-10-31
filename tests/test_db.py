from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    new_user = User(
        username='alison', password='secret123', email='teste@teste.com.br'
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'alison'))

    assert user.username == 'alison'
