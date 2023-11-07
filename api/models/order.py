from datetime import datetime
from models.database import db
from models.review import Review


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)

    delivery_date = db.Column(db.DateTime, nullable=False)
    order_reference_code = db.Column(db.String(50), nullable=True, unique=True)
    invoice = db.Column(db.String(100), nullable=True)
    payment_method = db.Column(db.String(50), nullable=True)
    number_of_items = db.Column(db.Integer, nullable=True)
    order_reference = db.Column(db.String(50), nullable=True, unique=True)
    booking_date = db.Column(db.DateTime, nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    booking_status = db.Column(db.String(50), nullable=False)
    total_price = db.Column(db.Float(precision=2), nullable=False)
    payment_status = db.Column(db.String(50), nullable=False)
    pickup_date_scheduled = db.Column(db.DateTime, nullable=False)
    pickup_date_actual = db.Column(db.DateTime, nullable=False)
    packed = db.Column(db.Boolean, nullable=False, default=True)
    pickup_address = db.Column(db.String(255), nullable=True)
    pickup_status = db.Column(db.Boolean, nullable=True)

    # New columns for shipment-related fields
    shipment_status = db.Column(db.String(50), nullable=True)
    shipment_tracking_number = db.Column(db.String(50), nullable=True)
    shipment_carrier = db.Column(db.String(50), nullable=True)
    shipment_eta = db.Column(db.DateTime, nullable=True)

    # Relationships
    user = db.relationship('User', back_populates='orders')
    reviews = db.relationship('Review', back_populates='order')

    # order_items = db.relationship(
    #     'OrderItem', back_populates='order', cascade="all, delete-orphan")
    # reviews = db.relationship('Review', back_populates='order')

    def __init__(self, user_id, delivery_date, total_price, packed, payment_status, pickup_status, pickup_address, pickup_date_scheduled, pickup_date_actual, order_reference_code=None, invoice=None, payment_method=None, number_of_items=None, booking_date=None, booking_status='Pending', shipment_status=None, shipment_tracking_number=None, shipment_carrier=None, shipment_eta=None):
        self.user_id = user_id
        self.delivery_date = delivery_date
        self.order_reference_code = order_reference_code
        self.invoice = invoice
        self.payment_method = payment_method
        self.number_of_items = number_of_items
        self.order_reference = f"ORDER-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        self.booking_date = booking_date if booking_date else datetime.utcnow()
        self.booking_status = booking_status
        self.order_date = datetime.utcnow()
        self.total_price = total_price
        self.payment_status = payment_status
        self.pickup_date_scheduled = pickup_date_scheduled
        self.pickup_date_actual = pickup_date_actual
        self.pickup_address = pickup_address
        self.pickup_status = pickup_status
        self.packed = packed
        self.shipment_status = shipment_status
        self.shipment_tracking_number = shipment_tracking_number
        self.shipment_carrier = shipment_carrier
        self.shipment_eta = shipment_eta

    def to_dict(self):
        return {
            'id': self.id,
            'order_date': self.order_date.isoformat(),
            'delivery_date': self.delivery_date.isoformat(),
            'total_price': self.total_price,
            'number_of_items': self.number_of_items,
            'invoice': self.invoice,
            'payment_method': self.payment_method,
            'booking_date': self.booking_date.isoformat(),
            'booking_status': self.booking_status,
            'payment_status': self.payment_status,
            'pickup_date_scheduled': self.pickup_date_scheduled.isoformat(),
            'pickup_date_actual': self.pickup_date_actual.isoformat(),
            'order_reference_code': self.order_reference_code,
            'packed': self.packed,
            'shipment_status': self.shipment_status,
            'shipment_tracking_number': self.shipment_tracking_number,
            'shipment_carrier': self.shipment_carrier,
            'shipment_eta': self.shipment_eta.isoformat() if self.shipment_eta else None
        }

    def __str__(self):
        return f"Order {self.order_reference} by {self.user.username}"
