
from datetime import datetime
from models.main import db


class WarehouseSpace(db.Model):
    __tablename__ = 'warehouse_spaces'

    space_id = db.Column(db.Integer, primary_key=True)
    capacity = db.Column(db.Float, nullable=False)
    availability = db.Column(db.Boolean, default=True)
    size = db.Column(db.String, nullable=False)
    # Add other space-related fields here

    # Define a one-to-many relationship with Stored Items
    stored_items = db.relationship(
        'StoredItem', backref='warehouse_space', lazy=True)
