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


# Creating pickup
@app.route('/pickup', methods=['POST'])
def create_pickup():
    if request.method == 'POST':
        # Extract pickup data from the POST request
        data = request.get_json()

        # Check if the required fields are present in the request
        required_fields = ['user_id', 'pickup_address', 'pickup_status']
        if all(field in data for field in required_fields):
            user_id = data['user_id']
            pickup_address = data['pickup_address']
            pickup_status = data['pickup_status']

            # Check if the user_id exists in the database
            user = User.query.get(user_id)
            if user is None:
                return jsonify({'error': 'User does not exist'}, 400)

            # Create a new Pickup object
            new_pickup = Pickup(
                user_id=user_id, pickup_address=pickup_address, pickup_status=pickup_status)

            # Add the new pickup to the database
            db.session.add(new_pickup)
            db.session.commit()

            return jsonify({'message': 'Pickup created successfully'})

        return jsonify({'error': 'Missing required fields'}, 400)

# Getting all pickups


@app.route('/pickup', methods=['GET'])
def get_all_pickups():
    # Query the database to retrieve all pickup objects
    pickups = Pickup.query.all()

    # Convert the pickups to a list of dictionaries
    pickup_list = []
    for pickup in pickups:
        pickup_dict = {
            'id': pickup.pickup_id,
            'user_id': pickup.user_id,
            'pickup_address': pickup.pickup_address,
            'pickup_status': pickup.pickup_status,
        }
        pickup_list.append(pickup_dict)

    return jsonify({'pickups': pickup_list})
# Getting single pickup


@app.route('/pickup/<int:pickup_id>', methods=['GET'])
def get_single_pickup(pickup_id):
    # Query the database to retrieve the pickup with the specified pickup_id
    pickup = Pickup.query.get(pickup_id)

    if pickup is None:
        return jsonify({'message': 'Pickup not found'}, 404)

    pickup_data = {
        'pickup_id': pickup.pickup_id,
        'user_id': pickup.user_id,
        'pickup_address': pickup.pickup_address,
        'pickup_status': pickup.pickup_status,
        # Add other fields from the Pickup model as needed
    }

    return jsonify(pickup_data)
