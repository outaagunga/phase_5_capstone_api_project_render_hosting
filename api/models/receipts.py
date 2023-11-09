from datetime import datetime
from models.main import db


class Receipt(db.Model):
    __tablename__ = 'receipts'

    receipt_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    transaction_id = db.Column(db.Integer, db.ForeignKey(
        'transactions.transaction_id'), nullable=False)
    # e.g., Storage, Delivery, Pickup
    receipt_type = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    # Add other receipt-related fields here

    # Define a many-to-one relationship with User
    user = db.relationship('User', backref='receipts')

    # Define a many-to-one relationship with Transaction
    transaction = db.relationship('Transaction', backref='receipts')
