from datetime import datetime
from models.main import db


class Pickup(db.Model):
    __tablename__ = 'pickups'

    pickup_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    pickup_address = db.Column(db.String(255), nullable=False)
    # Pending, Completed, etc.
    pickup_status = db.Column(db.String(20), default='Pending')
    # Add other pickup-related fields here

    # Define a one-to-many relationship with Transactions
    transactions = db.relationship(
        'Transaction', back_populates='pickup', lazy=True)
