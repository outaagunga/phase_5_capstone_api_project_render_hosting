from datetime import datetime
from models.main import db


class Delivery(db.Model):
    __tablename__ = 'deliveries'

    delivery_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    delivery_address = db.Column(db.String(255), nullable=False)
    # Pending, Delivered, etc.
    delivery_status = db.Column(db.String(20), default='Pending')
    # Add other delivery-related fields here

    # Define a one-to-many relationship with Transactions
    transactions = db.relationship(
        'Transaction', back_populates='delivery', lazy=True)
    # user = db.relationship('User', back_populates='deliveries')
