from ast import parse
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

# Creating inventory


@app.route('/inventory', methods=['POST'])
def create_inventory():
    if request.method == 'POST':
        # Extract inventory data from the POST request
        data = request.get_json()

        # Check if the required fields are present in the request
        required_fields = ['item_id', 'item_name', 'quantity']
        if all(field in data for field in required_fields):
            item_id = data['item_id']
            item_name = data['item_name']
            item_type = data.get('item_type')  # Optional field
            quantity = data['quantity']
            date_to_warehouse_str = data.get(
                'date_to_warehouse')  # Optional field
            description = data.get('description')  # Optional field

            # Parse the date_to_warehouse string into a datetime object if provided
            if date_to_warehouse_str:
                date_to_warehouse = datetime.fromisoformat(
                    date_to_warehouse_str)
            else:
                date_to_warehouse = None

            # You can add additional validation here if needed

            # Optional: Check if the item exists before creating the inventory entry
            item = StoredItem.query.get(item_id)

            if item is None:
                return jsonify({'error': 'Item does not exist'}, 400)

            # Create a new Inventory object with relevant fields
            new_inventory = Inventory(
                item_id=item_id,
                item_name=item_name,
                item_type=item_type,
                quantity=quantity,
                date_to_warehouse=date_to_warehouse,
                description=description
                # Add other relevant fields from your Inventory model here if needed
            )

            # Add the new inventory entry to the database
            db.session.add(new_inventory)
            db.session.commit()

            return jsonify({'message': 'Inventory created successfully'})

        return jsonify({'error': 'Missing required fields'}, 400)
