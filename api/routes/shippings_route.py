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

# Creating shipping


@app.route('/shipping', methods=['POST'])
def create_shipping():
    if request.method == 'POST':
        # Extract shipping data from the POST request
        data = request.get_json()

        # Check if the required fields are present in the request
        required_fields = ['user_id', 'shipping_address']
        if all(field in data for field in required_fields):
            user_id = data['user_id']
            shipping_address = data['shipping_address']

            # Check if the user with the provided user_id exists
            user = User.query.get(user_id)
            if user is None:
                return jsonify({'error': 'User does not exist'}, 400)

            # Create a new Shipping object with all the required fields
            new_shipping = Shipping(
                user_id=user_id,
                shipping_address=shipping_address,
                # You can include other fields here
                shipping_status=data.get('shipping_status', 'Pending')
            )

            # Add the new shipping record to the database
            db.session.add(new_shipping)
            db.session.commit()

            return jsonify({'message': 'Shipping record created successfully'})

        return jsonify({'error': 'Missing required fields'}, 400)


# Getting all shippings
@app.route('/shippings', methods=['GET'])
def get_all_shippings():
    if request.method == 'GET':
        # Query the database to retrieve all shipping records
        all_shippings = Shipping.query.all()

        # Serialize the shipping records to a list of dictionaries
        shipping_list = []
        for shipping in all_shippings:
            shipping_data = {
                'shipping_id': shipping.shipping_id,
                'user_id': shipping.user_id,
                'shipping_address': shipping.shipping_address,
                'shipping_status': shipping.shipping_status,
                # Include other fields here
            }
            shipping_list.append(shipping_data)

        return jsonify({'shippings': shipping_list})

# Getting single shipping records


@app.route('/shippings/<int:shipping_id>', methods=['GET'])
def get_single_shipping(shipping_id):
    if request.method == 'GET':
        # Query the database to retrieve the shipping record with the specified shipping_id
        shipping = Shipping.query.get(shipping_id)

        if shipping is None:
            return jsonify({'message': 'Shipping record not found'}, 404)

        shipping_data = {
            'shipping_id': shipping.shipping_id,
            'user_id': shipping.user_id,
            'shipping_address': shipping.shipping_address,
            'shipping_status': shipping.shipping_status,
            # Include other fields from the Shipping model as needed
        }

        return jsonify(shipping_data)
