
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

# Creating transactions


@app.route('/transaction', methods=['POST'])
def create_transaction():
    if request.method == 'POST':
        # Extract transaction data from the POST request
        data = request.get_json()

        # Check if the required fields are present in the request
        required_fields = ['user_id', 'item_id', 'type', 'timestamp']
        if all(field in data for field in required_fields):
            user_id = data['user_id']
            item_id = data['item_id']
            transaction_type = data['type']

            # Parse the timestamp string into a datetime object
            timestamp_str = data['timestamp']
            timestamp = datetime.fromisoformat(timestamp_str)

            # You can add additional validation here if needed

            # Optional: Check if the user and item exist before creating the transaction
            user = User.query.get(user_id)
            item = StoredItem.query.get(item_id)

            if user is None or item is None:
                return jsonify({'error': 'User or item does not exist'}, 400)

            # Create a new Transaction object with relevant fields
            new_transaction = Transaction(
                user_id=user_id,
                item_id=item_id,
                type=transaction_type,
                timestamp=timestamp
                # Add other relevant fields from your Transaction model here if needed
            )

            # Add the new transaction to the database
            db.session.add(new_transaction)
            db.session.commit()

            return jsonify({'message': 'Transaction created successfully'})

        return jsonify({'error': 'Missing required fields'}, 400)


# gGetting transactions
@app.route('/transactions', methods=['GET'])
def get_all_transactions():
    if request.method == 'GET':
        # Query all transactions from the database
        transactions = Transaction.query.all()

        if not transactions:
            return jsonify({'message': 'No transactions found'})

        # Convert the list of transactions to a list of dictionaries for JSON serialization
        transactions_list = [
            {
                'transaction_id': transaction.transaction_id,
                'user_id': transaction.user_id,
                'item_id': transaction.item_id,
                'type': transaction.type,
                'timestamp': transaction.timestamp.isoformat(),  # Convert to ISO format
                # Include other relevant fields as needed
            }
            for transaction in transactions
        ]

        return jsonify(transactions_list)

# Getting single transaction


@app.route('/transactions/<int:transaction_id>', methods=['GET'])
def get_single_transaction(transaction_id):
    if request.method == 'GET':
        # Query the database to retrieve the transaction with the specified transaction_id
        transaction = Transaction.query.get(transaction_id)

        if transaction is None:
            return jsonify({'message': 'Transaction not found'}, 404)

        transaction_data = {
            'transaction_id': transaction.transaction_id,
            'user_id': transaction.user_id,
            'item_id': transaction.item_id,
            'type': transaction.type,
            'timestamp': transaction.timestamp.isoformat(),  # Convert to ISO format
            # Include other relevant fields as needed
        }

        return jsonify(transaction_data)
