from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from .db import db


class Point(db.Model):
    __tablename__ = 'points'

    id = db.Column(UUID(), primary_key=True, default=uuid4, server_default=func.uuid_generate_v4())
    year = db.Column(db.String(), nullable=False)
    mstet = db.Column(db.String(), nullable=False)
    ltc = db.Column(db.String(), nullable=False)
    place = db.Column(db.String(), nullable=False)
    address = db.Column(db.String(), nullable=False)
    client = db.Column(db.String(), nullable=False)
    project_price_predict = db.Column(db.Numeric(precision=11, scale=4, asdecimal=False), nullable=True)
    comment = db.Column(db.String(), nullable=True)

    latitude = db.Column(db.Integer(), nullable=True)
    longitude = db.Column(db.Integer(), nullable=True)

    failure = db.Column(db.Boolean(), nullable=False)
    date_failure = db.Column(db.DateTime(), nullable=True)

    application_source = db.Column(db.String(), nullable=True)

    hermes_number = db.Column(db.Integer(), nullable=True)
    hermes_deadline = db.Column(db.DateTime(), nullable=True)
    hermes_smr_successful = db.Column(db.Boolean(), nullable=True)

    brigadier = db.Column(db.String(), nullable=True)
    project_engineer = db.Column(db.String(), nullable=True)

    smr = db.Column(db.Boolean(), nullable=True)
    svarka = db.Column(db.Boolean(), nullable=True)
    subcontracting_price = db.Column(db.Numeric(precision=11, scale=4, asdecimal=False), nullable=True)
    material_price = db.Column(db.Numeric(precision=11, scale=4, asdecimal=False), nullable=True)
    ks11_signed_by_ltc = db.Column(db.Boolean(), nullable=True)
    project_price_ks2 = db.Column(db.Numeric(precision=11, scale=4, asdecimal=False), nullable=True)
    date_ks2 = db.Column(db.DateTime(), nullable=True)
    google_doc_link = db.Column(db.String(), nullable=True)

    user_id = db.Column(UUID(), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True, index=True, comment='ID пользователя')  # noqa)