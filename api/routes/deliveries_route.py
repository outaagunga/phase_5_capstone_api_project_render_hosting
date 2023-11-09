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

# Creating Delevery


@app.route('/delivery', methods=['POST'])
def create_delivery():
    if request.method == 'POST':
        # Extract delivery data from the POST request
        data = request.get_json()

        # Check if the required fields are present in the request
        required_fields = ['user_id', 'delivery_address']
        if all(field in data for field in required_fields):
            user_id = data['user_id']
            delivery_address = data['delivery_address']

            # Check if the user with the given user_id exists
            user = User.query.get(user_id)
            if user is None:
                return jsonify({'error': 'User not found'}, 404)

            # Create a new Delivery object
            new_delivery = Delivery(
                user_id=user_id,
                delivery_address=delivery_address
                # You can add more fields as needed
            )

            # Add the new delivery to the database
            db.session.add(new_delivery)
            db.session.commit()

            return jsonify({'message': 'Delivery created successfully'})

        return jsonify({'error': 'Missing required fields'}, 400)

# Getting all deliveires


@app.route('/deliveries', methods=['GET'])
def get_deliveries():
    if request.method == 'GET':
        # Retrieve all delivery records from the database
        deliveries = Delivery.query.all()

        # Convert the delivery records to a list of dictionaries
        delivery_list = []
        for delivery in deliveries:
            delivery_dict = {
                'delivery_id': delivery.delivery_id,
                'user_id': delivery.user_id,
                'delivery_address': delivery.delivery_address,
                'delivery_status': delivery.delivery_status,
                # Add other fields from the Delivery model as needed
            }
            delivery_list.append(delivery_dict)

        return jsonify(delivery_list)
# Getting single deleivery


@app.route('/deliveries/<int:delivery_id>', methods=['GET'])
def get_single_delivery(delivery_id):
    if request.method == 'GET':
        # Query the database to retrieve the delivery with the specified delivery_id
        delivery = Delivery.query.filter_by(delivery_id=delivery_id).first()

        if delivery is None:
            return jsonify({'message': 'Delivery not found'}, 404)

        delivery_data = {
            'delivery_id': delivery.delivery_id,
            'user_id': delivery.user_id,
            'delivery_address': delivery.delivery_address,
            'delivery_status': delivery.delivery_status,
            # Add other fields from the Delivery model as needed
        }

        return jsonify(delivery_data)
