from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from .db import db


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(UUID(), primary_key=True, default=uuid4, server_default=func.uuid_generate_v4())
    year = db.Column(db.String(), nullable=False)
    mstet = db.Column(db.String(), nullable=False)
    ltc = db.Column(db.String(), nullable=False)
    place = db.Column(db.String(), nullable=False)
    address = db.Column(db.String(), nullable=False)
    client = db.Column(db.String(), nullable=False)
    project_price_predict = db.Column(db.Numeric(precision=11, scale=4, asdecimal=False), nullable=True)
    comment = db.Column(db.String(), nullable=True)

    latitude = db.Column(db.Float(), nullable=True)
    longitude = db.Column(db.Float(), nullable=True)

    google_doc_link = db.Column(db.String(), nullable=True)

    user_id = db.Column(UUID(), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True, index=True, comment='ID пользователя')  # noqa)
    activate = db.Column(db.Boolean(), nullable=False, default=True)
