
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


# creating space
@app.route('/space', methods=['POST'])
def create_warehouse_space():
    if request.method == 'POST':
        # Extract warehouse space data from the POST request
        data = request.get_json()

        # Check if the required fields are present in the request
        required_fields = ['capacity', 'availability', 'size']
        if all(field in data for field in required_fields):
            capacity = data['capacity']
            availability = data['availability']
            size = data['size']

            # Create a new WarehouseSpace object
            new_warehouse_space = WarehouseSpace(
                capacity=capacity, availability=availability, size=size)

            # Add the new warehouse space to the database
            db.session.add(new_warehouse_space)
            db.session.commit()

            return jsonify({'message': 'Warehouse space created successfully'})

        return jsonify({'error': 'Missing required fields'}, 400)

# Getting all warehouse space


@app.route('/spaces', methods=['GET'])
def get_available_warehouse_spaces():
    if request.method == 'GET':
        # Query the database for warehouse spaces with availability set to True
        available_spaces = WarehouseSpace.query.filter_by(
            availability=True).all()

        # Prepare the response data
        space_list = []
        for space in available_spaces:
            space_data = {
                'space_id': space.space_id,
                'capacity': space.capacity,
                'size': space.size,
                # Add other space-related fields as needed
            }
            space_list.append(space_data)

        return jsonify({'available_spaces': space_list})
# Getting a single ware house details


@app.route('/spaces/<int:space_id>', methods=['GET'])
def get_single_warehouse_space(space_id):
    if request.method == 'GET':
        # Query the database to retrieve the warehouse space with the specified space_id
        warehouse_space = WarehouseSpace.query.get(space_id)

        if warehouse_space is None:
            return jsonify({'message': 'Warehouse space not found'}, 404)

        warehouse_space_data = {
            'space_id': warehouse_space.space_id,
            'capacity': warehouse_space.capacity,
            'size': warehouse_space.size,
            # Add other space-related fields as needed
        }

        return jsonify(warehouse_space_data)
