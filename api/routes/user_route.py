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


# Creating a user:
@app.route('/user', methods=['POST'])
def create_user():
    if request.method == 'POST':
        # Extract user data from the POST request
        data = request.get_json()

        # Check if the required fields are present in the request
        required_fields = ['username', 'password', 'email']
        if all(field in data for field in required_fields):
            username = data['username']
            raw_password = data['password']
            email = data['email']

            # Check if a user with the same username or email already exists
            if User.query.filter((User.username == username) | (User.email == email)).first():
                return jsonify({'error': 'Username or email already exists'}, 400)

            # Hash the password using generate_password_hash
            password_hash = generate_password_hash(
                raw_password, method='pbkdf2:sha256')

            # Create a new User object with the hashed password
            new_user = User(username=username,
                            password=password_hash, email=email)

            # Add the new user to the database
            db.session.add(new_user)
            db.session.commit()

            return jsonify({'message': 'User created successfully'})

        return jsonify({'error': 'Missing required fields'}, 400)


# get all users


@app.route('/users', methods=['GET'])
def get_all_users():
    if request.method == 'GET':
        # Query the database to retrieve all users and their related data
        users = User.query.all()

        if not users:
            return jsonify({'message': 'No users found'}, 200)

        user_list = []
        for user in users:
            user_data = {
                'user_id': user.user_id,
                'username': user.username,
                'email': user.email,
                'stored_items': [],
                'transactions': [],
                'deliveries': [],
                'pickups': [],
                'shipping': [],
                'receipts': [],
                'warehouse': []
            }

            # Collect stored items related to the user
            for stored_item in user.stored_items:
                stored_item_data = {
                    'item_id': stored_item.item_id,
                    'item_name': stored_item.item_name,
                    'status': stored_item.status,
                    # Add other stored item fields as needed
                }
                user_data['stored_items'].append(stored_item_data)

            # Collect transactions related to the user
            for transaction in user.transactions:
                transaction_data = {
                    'transaction_id': transaction.transaction_id,
                    'type': transaction.type,
                    'timestamp': transaction.timestamp,
                    # Add other transaction fields as needed
                }
                user_data['transactions'].append(transaction_data)

            # Collect deliveries related to the user
            for delivery in user.deliveries:
                delivery_data = {
                    'delivery_id': delivery.delivery_id,
                    'delivery_address': delivery.delivery_address,
                    'delivery_status': delivery.delivery_status,
                    # Add other delivery fields as needed
                }
                user_data['deliveries'].append(delivery_data)

            # Collect pickups related to the user
            for pickup in user.pickups:
                pickup_data = {
                    'pickup_id': pickup.pickup_id,
                    'pickup_address': pickup.pickup_address,
                    'pickup_status': pickup.pickup_status,
                    # Add other pickup fields as needed
                }
                user_data['pickups'].append(pickup_data)

            # Collect shipping related to the user
            for shipping in user.shipping:
                shipping_data = {
                    'shipping_id': shipping.shipping_id,
                    'shipping_address': shipping.shipping_address,
                    'shipping_status': shipping.shipping_status,
                    # Add other shipping fields as needed
                }
                user_data['shipping'].append(shipping_data)

            # Collect receipts related to the user
            for receipt in user.receipts:
                receipt_data = {
                    'receipt_id': receipt.receipt_id,
                    'receipt_type': receipt.receipt_type,
                    'timestamp': receipt.timestamp,
                    'amount': receipt.amount,
                    # Add other receipt fields as needed
                }
                user_data['receipts'].append(receipt_data)

            user_list.append(user_data)

        return jsonify({'users': user_list}, 200)

# Getting single user


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    if request.method == 'GET':
        # Query the database to retrieve the user with the specified user_id
        user = User.query.filter_by(user_id=user_id).first()

        if user is None:
            return jsonify({'message': 'User not found'}, 404)

        user_data = {
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'stored_items': [],
            'transactions': [],
            'deliveries': [],
            'pickups': [],
            'shipping': [],
            'receipts': [],
            'warehouse': []
        }

        # Collect stored items related to the user
        for stored_item in user.stored_items:
            stored_item_data = {
                'item_id': stored_item.item_id,
                'item_name': stored_item.item_name,
                'status': stored_item.status,
                # Add other stored item fields as needed
            }
            user_data['stored_items'].append(stored_item_data)

        # Collect transactions related to the user
        for transaction in user.transactions:
            transaction_data = {
                'transaction_id': transaction.transaction_id,
                'type': transaction.type,
                'timestamp': transaction.timestamp,
                # Add other transaction fields as needed
            }
            user_data['transactions'].append(transaction_data)

        # Collect deliveries related to the user
        for delivery in user.deliveries:
            delivery_data = {
                'delivery_id': delivery.delivery_id,
                'delivery_address': delivery.delivery_address,
                'delivery_status': delivery.delivery_status,
                # Add other delivery fields as needed
            }
            user_data['deliveries'].append(delivery_data)

        # Collect pickups related to the user
        for pickup in user.pickups:
            pickup_data = {
                'pickup_id': pickup.pickup_id,
                'pickup_address': pickup.pickup_address,
                'pickup_status': pickup.pickup_status,
                # Add other pickup fields as needed
            }
            user_data['pickups'].append(pickup_data)

        # Collect shipping related to the user
        for shipping in user.shipping:
            shipping_data = {
                'shipping_id': shipping.shipping_id,
                'shipping_address': shipping.shipping_address,
                'shipping_status': shipping.shipping_status,
                # Add other shipping fields as needed
            }
            user_data['shipping'].append(shipping_data)

        # Collect receipts related to the user
        for receipt in user.receipts:
            receipt_data = {
                'receipt_id': receipt.receipt_id,
                'receipt_type': receipt.receipt_type,
                'timestamp': receipt.timestamp,
                'amount': receipt.amount,
                # Add other receipt fields as needed
            }
            user_data['receipts'].append(receipt_data)

        return jsonify({'user': user_data}, 200)


# # Route to get single user
# @app.route('/user/<int:user_id>', methods=['GET'])
# def get_user(user_id):
#     try:
#         # Find the user by user ID
#         user = User.query.get(user_id)

#         if not user:
#             return jsonify({'error': 'User not found'}), 404

#         # Create a user data dictionary
#         user_data = {
#             'user_id': user.user_id,
#             'public_id': user.public_id,
#             'full_name': user.full_name,
#             'username': user.username,
#             'email': user.email,
#             'phone_number': user.phone_number,
#             'profile_picture': user.profile_picture,
#             'address': user.address,
#             'role': user.role,
#             'date_of_birth': user.date_of_birth.isoformat() if user.date_of_birth else None,
#             'gender': user.gender,
#             'bio': user.bio,
#             'orders': [],
#             'storage_units': []
#         }

#         # Extract user's orders
#         orders = user.orders
#         for order in orders:
#             order_data = {
#                 'id': order.id,
#                 'order_date': order.order_date.isoformat(),
#                 'delivery_date': order.delivery_date.isoformat(),
#                 'total_price': order.total_price,
#                 'number_of_items': order.number_of_items,
#                 'invoice': order.invoice,
#                 'payment_method': order.payment_method,
#                 'booking_date': order.booking_date.isoformat(),
#                 'booking_status': order.booking_status,
#                 'payment_status': order.payment_status,
#                 'pickup_date_scheduled': order.pickup_date_scheduled.isoformat(),
#                 'pickup_date_actual': order.pickup_date_actual.isoformat(),
#                 'order_reference_code': order.order_reference_code,
#                 'packed': order.packed,
#                 'shipment_status': order.shipment_status,
#                 'shipment_tracking_number': order.shipment_tracking_number,
#                 'shipment_carrier': order.shipment_carrier,
#                 'shipment_eta': order.shipment_eta.isoformat() if order.shipment_eta else None
#             }
#             user_data['orders'].append(order_data)

#         # Extract user's storage units (if they exist)
#         if hasattr(user, 'storage_units'):
#             storage_units = user.storage_units
#             for storage_unit in storage_units:
#                 storage_unit_data = {
#                     'id': storage_unit.id,
#                     'name': storage_unit.name,
#                     'description': storage_unit.description,
#                     'size': storage_unit.size,
#                     'capacity': storage_unit.capacity,
#                     'price_per_month': storage_unit.price_per_month,
#                     'available': storage_unit.available,
#                     'address': storage_unit.address,
#                     'latitude': storage_unit.latitude,
#                     'longitude': storage_unit.longitude
#                 }
#                 user_data['storage_units'].append(storage_unit_data)

#         # Return the user data as JSON
#         return jsonify(user_data)

#     except Exception as e:
#         return jsonify({'error': str(e)})


# # Deleting a user
# @app.route('/users/<int:user_id>', methods=['DELETE'])
# # @token_required
# def delete_user(user_id):
#     try:
#         # Query the user by user_id
#         user = User.query.get(user_id)

#         if user is not None:
#             # Delete the user from the database
#             db.session.delete(user)
#             db.session.commit()

#             return jsonify({'message': 'User deleted successfully'})

#         return jsonify({'message': 'User not found'}), 404

#     except Exception as e:
#         return jsonify({'error': str(e)})


# # Updating a user details:
# @app.route('/user/<int:user_id>', methods=['PUT'])
# def update_user(user_id):
#     data = request.get_json()

#     # Retrieve the user from the database based on the user_id
#     user = User.query.get(user_id)

#     if not user:
#         return jsonify({'error': 'User not found'}), 404

#     try:
#         if 'full_name' in data:
#             user.full_name = data['full_name']

#         if 'username' in data:
#             # Check for a unique username
#             existing_user = User.query.filter_by(
#                 username=data['username']).first()
#             if existing_user and existing_user.user_id != user.user_id:
#                 return jsonify({'error': 'Username is already taken'}), 409
#             user.username = data['username']

#         if 'email' in data:
#             # Check for a unique email
#             existing_email = User.query.filter_by(email=data['email']).first()
#             if existing_email and existing_email.user_id != user.user_id:
#                 return jsonify({'error': 'Email is already in use'}), 409
#             user.email = data['email']

#         if 'phone_number' in data:
#             user.phone_number = data['phone_number']

#         if 'role' in data:
#             user.role = data['role']

#         if 'profile_picture' in data:
#             user.profile_picture = data['profile_picture']

#         if 'address' in data:
#             user.address = data['address']

#         if 'bio' in data:
#             user.bio = data['bio']

#         if 'password' in data:
#             # password hashed
#             hashed_password = generate_password_hash(
#                 data['password'], method='pbkdf2:sha256')
#             user.password = hashed_password

#         if 'date_of_birth' in data:
#             # Parse and convert the date_of_birth string to a Python date object
#             date_of_birth_str = data['date_of_birth']
#             date_of_birth = None

#             if date_of_birth_str:
#                 try:
#                     date_of_birth = datetime.strptime(
#                         date_of_birth_str, '%Y-%m-%d').date()
#                 except ValueError:
#                     # Handle invalid date format here, e.g., return an error response
#                     return jsonify({'error': 'Invalid date of birth format. Please use YYYY-MM-DD'}), 400

#             user.date_of_birth = date_of_birth

#         if 'gender' in data:
#             user.gender = data['gender']

#         db.session.commit()

#         updated_user_data = {
#             'user_id': user.user_id,
#             'full_name': user.full_name,
#             'username': user.username,
#             'email': user.email,
#             'phone_number': user.phone_number,
#             'role': user.role,
#             'profile_picture': user.profile_picture,
#             'address': user.address,
#             'bio': user.bio,
#             'date_of_birth': user.date_of_birth.strftime('%Y-%m-%d'),
#             'gender': user.gender,
#         }

#         return jsonify({'message': 'User updated successfully', 'user': updated_user_data})
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': 'User update failed. Please try again later.'}), 500
