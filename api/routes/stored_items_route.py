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

# Creating stored item


@app.route('/stored_item', methods=['POST'])
def create_stored_item():
    if request.method == 'POST':
        # Extract stored item data from the POST request
        data = request.get_json()

        # Check if the required fields are present in the request
        required_fields = ['user_id', 'space_id', 'item_name']
        if all(field in data for field in required_fields):
            user_id = data['user_id']
            space_id = data['space_id']
            item_name = data['item_name']
            description = data.get('description', '')
            image = data.get('image', '')

            status = data.get('status', 'In')

            # Check if the user and warehouse space exist
            user = User.query.get(user_id)
            space = WarehouseSpace.query.get(space_id)

            if user is None or space is None:
                return jsonify({'error': 'User or space not found'}, 404)

            # Create a new StoredItem object
            new_item = StoredItem(user_id=user_id, space_id=space_id, item_name=item_name,
                                  description=description, image=image, status=status)

            # Add the new item to the database
            db.session.add(new_item)
            db.session.commit()

            return jsonify({'message': 'Stored item created successfully'})

        return jsonify({'error': 'Missing required fields'}, 400)


# Getting all stored items
@app.route('/stored_items', methods=['GET'])
def get_all_stored_items():
    if request.method == 'GET':
        # Query the database for all stored items
        stored_items = StoredItem.query.all()

        # Prepare the response data
        item_list = []
        for item in stored_items:
            item_data = {
                'item_id': item.item_id,
                'user_id': item.user_id,
                'space_id': item.space_id,
                'item_name': item.item_name,
                'description': item.description,
                'image': item.image,
                'status': item.status,
                # Add other item-related fields as needed
            }
            item_list.append(item_data)

        return jsonify({'stored_items': item_list})

# Getting single stored item


@app.route('/stored_items/<int:item_id>', methods=['GET'])
def get_single_stored_item(item_id):
    if request.method == 'GET':
        # Query the database to retrieve the stored item with the specified item_id
        stored_item = StoredItem.query.get(item_id)

        if stored_item is None:
            return jsonify({'message': 'Stored item not found'}, 404)

        stored_item_data = {
            'item_id': stored_item.item_id,
            'user_id': stored_item.user_id,
            'space_id': stored_item.space_id,
            'item_name': stored_item.item_name,
            'description': stored_item.description,
            'image': stored_item.image,
            'status': stored_item.status,
            # Add other item-related fields as needed
        }

        return jsonify(stored_item_data)
