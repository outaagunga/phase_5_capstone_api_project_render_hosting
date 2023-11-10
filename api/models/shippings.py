from datetime import datetime
from models.main import db


class Shipping(db.Model):
    __tablename__ = 'shippings'

    shipping_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    shipping_address = db.Column(db.String(255), nullable=False)
    # Pending, Shipped, Delivered, etc.
    shipping_status = db.Column(db.String(20), default='Pending')
    # Add other shipping-related fields here

    # Define a one-to-many relationship with Transactions
    transactions = db.relationship(
        'Transaction', back_populates='shipping')
