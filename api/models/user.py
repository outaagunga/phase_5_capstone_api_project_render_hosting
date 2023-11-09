
from datetime import datetime
from models.main import db


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    # Add other user-related fields here

    # Define a one-to-many relationship with Stored Items
    stored_items = db.relationship('StoredItem', backref='user', lazy=True)
    transactions = db.relationship('Transaction', backref='user', lazy=True)
    deliveries = db.relationship('Delivery', backref='user', lazy=True)
    pickups = db.relationship('Pickup', backref='user', lazy=True)
    shipping = db.relationship('Shipping', backref='user', lazy=True)
