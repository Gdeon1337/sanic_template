from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from .db import db


class OrderUsers(db.Model):
    __tablename__ = 'order_users'

    id = db.Column(UUID(), primary_key=True, default=uuid4, server_default=func.uuid_generate_v4(), comment='ID')  # noqa
    auction_price = db.Column(db.Float(), nullable=True)
    google_disk_link = db.Column(db.String(), nullable=True)
    user_id = db.Column(UUID(), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True, index=True, comment='ID пользователя')  # noqa)
    order_id = db.Column(UUID(), db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=True, index=True, comment='ID заказа')  # noqa)
