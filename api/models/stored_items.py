from datetime import datetime
from models.main import db


class StoredItem(db.Model):
    __tablename__ = 'stored_items'

    item_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    space_id = db.Column(db.Integer, db.ForeignKey(
        'warehouse_spaces.space_id'), nullable=False)
    item_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(255))  # Store the path to the image
    status = db.Column(db.String(20), default='In')  # In, Out, etc.
    # Add other item-related fields here

    # Define a one-to-many relationship with Transactions
    transactions = db.relationship(
        'Transaction', back_populates='stored_item', lazy=True)
