from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from .db import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(), primary_key=True, default=uuid4, server_default=func.uuid_generate_v4(), comment='ID пользователя')  # noqa

    email = db.Column(db.String(), nullable=True, comment='почта пользователя')  # noqa
    phone = db.Column(db.String(), nullable=True, comment='телефон пользователя')  # noqa
    name = db.Column(db.String(), nullable=True, comment='имя пользователя')  # noqa
    login = db.Column(db.String(), nullable=False, comment='Логин пользователя')  # noqa
    password = db.Column(db.LargeBinary(), nullable=False, comment='Пароль пользователя')  # noqa
