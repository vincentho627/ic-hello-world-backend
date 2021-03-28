import datetime
from ..database import database as db


def _get_date():
    return datetime.datetime.now()


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    contact_email = db.Column(db.String(120), nullable=True)
    contact_number = db.Column(db.String(20), nullable=True)
    date = db.Column(db.Date, default=_get_date)
    last_seen_location = db.Column(db.String(120), nullable=True)
    image_path = db.Column(db.String(100), nullable=True)
    found = db.Column(db.Boolean, default=False)
