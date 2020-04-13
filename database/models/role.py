from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from .db import db


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(UUID(), primary_key=True, default=uuid4, server_default=func.uuid_generate_v4(), comment='ID роли')  # noqa
    name = db.Column(db.String(), nullable=False, comment='Название роли')  # noqa
