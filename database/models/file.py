from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from .db import db


class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(UUID(), primary_key=True, default=uuid4, server_default=func.uuid_generate_v4(), comment='ID пользователя')  # noqa

    file_type = db.Column(db.String(), nullable=True)
    file_name = db.Column(db.String(), nullable=True)  # noqa
    file_data = db.Column(db.LargeBinary(), nullable=True)  # noqa
