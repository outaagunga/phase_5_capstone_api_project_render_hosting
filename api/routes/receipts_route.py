
from collections import OrderedDict
from datetime import datetime
import uuid
from psycopg2 import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request
from models.main import app, db
from models.transactions import Transaction
from models.inventory import Inventory
from models.deliveries import Delivery
from models.pickups import Pickup
from models.receipts import Receipt
from models.shippings import Shipping
from models.stored_items import StoredItem
from models.warehouse import WarehouseSpace
from models.user import User

# Creating receipts


@app.route('/receipt', methods=['POST'])
def create_receipt():
    if request.method == 'POST':
        # Extract receipt data from the POST request
        data = request.get_json()

        # Check if the required fields are present in the request
        required_fields = ['user_id', 'transaction_id',
                           'receipt_type', 'timestamp', 'amount']
        if all(field in data for field in required_fields):
            user_id = data['user_id']
            transaction_id = data['transaction_id']

            # Check if the associated transaction exists in the database
            transaction = Transaction.query.get(transaction_id)
            if transaction is None:
                return jsonify({'error': 'Transaction not found'}, 404)

            receipt_type = data['receipt_type']

            # Convert the timestamp string to a Python datetime object
            timestamp_str = data['timestamp']
            timestamp = datetime.fromisoformat(timestamp_str)

            amount = data['amount']

            # Check if the associated user exists in the database
            user = User.query.get(user_id)
            if user is None:
                return jsonify({'error': 'User not found'}, 404)

            # Create a new Receipt object
            new_receipt = Receipt(
                user_id=user_id,
                transaction_id=transaction_id,
                receipt_type=receipt_type,
                timestamp=timestamp,
                amount=amount
            )

            # Add the new receipt to the database
            db.session.add(new_receipt)
            db.session.commit()

            return jsonify({'message': 'Receipt created successfully'})

        return jsonify({'error': 'Missing required fields'}, 400)


# Getting all receipts
@app.route('/receipts', methods=['GET'])
def get_all_receipts():
    if request.method == 'GET':
        # Query the database to get all receipts
        receipts = Receipt.query.all()

        # Convert the receipts to a list of dictionaries
        receipts_list = []
        for receipt in receipts:
            receipts_list.append({
                'receipt_id': receipt.receipt_id,
                'user_id': receipt.user_id,
                'transaction_id': receipt.transaction_id,
                'receipt_type': receipt.receipt_type,
                'timestamp': receipt.timestamp.isoformat(),  # Convert datetime to ISO format
                'amount': receipt.amount
            })

        return jsonify(receipts_list)
