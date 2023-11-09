from datetime import datetime
from models.main import db


class Inventory(db.Model):
    __tablename__ = 'inventory'

    inventory_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey(
        'stored_items.item_id'), nullable=False, unique=True)
    item_name = db.Column(db.String(255), nullable=False)
    item_type = db.Column(db.String(100), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    # Set default to current timestamp
    date_to_warehouse = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=True)
    description = db.Column(db.Text, nullable=True)

    stored_item = db.relationship(
        'StoredItem', backref='inventory', uselist=False)
