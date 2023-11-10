from datetime import datetime
from models.main import db


class Transaction(db.Model):
    __tablename__ = 'transactions'

    transaction_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey(
        'stored_items.item_id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # In or Out
    timestamp = db.Column(db.DateTime, nullable=False)
    # Add other transaction-related fields here

    delivery_id = db.Column(
        db.Integer, db.ForeignKey('deliveries.delivery_id'))
    pickup_id = db.Column(db.Integer, db.ForeignKey('pickups.pickup_id'))
    shipping_id = db.Column(db.Integer, db.ForeignKey('shippings.shipping_id'))

    stored_item = db.relationship(
        'StoredItem', back_populates='transactions', lazy=True)
    # delivery = db.relationship(
    #     'Delivery', back_populates='transaction', uselist=False)
    # pickup = db.relationship(
    #     'Pickup', back_populates='transaction', uselist=False)
    shipping = db.relationship(
        'Shipping', back_populates='transactions', uselist=False)
    # user = db.relationship('User', back_populates='user_transactions')
