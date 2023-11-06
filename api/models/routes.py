# app.py
from flask import jsonify, request
from flask import jsonify
from flask import request, jsonify, make_response, session, redirect
from flask_migrate import Migrate
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
from models.user import User
from models.order import Order
# from app import app
from models.database import db, app


# Home Page
@app.route('/')
def home():
    return "Welcome to Jeco API"


# Getting all users
@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        # Query all users
        users = User.query.all()

        # Create a list to store user data dictionaries
        user_list = []

        for user in users:
            # Create a user data dictionary
            user_data = {
                'user_id': user.user_id,
                'public_id': user.public_id,
                'full_name': user.full_name,
                'username': user.username,
                'email': user.email,
                'phone_number': user.phone_number,
                'profile_picture': user.profile_picture,
                'address': user.address,
                'role': user.role,
                'date_of_birth': user.date_of_birth.isoformat() if user.date_of_birth else None,
                'gender': user.gender,
                'bio': user.bio,
                'orders': [],
                'storage_units': []
            }

            # Extract user's orders
            orders = user.orders
            for order in orders:
                order_data = {
                    'id': order.id,
                    'order_date': order.order_date.isoformat(),
                    'delivery_date': order.delivery_date.isoformat(),
                    'total_price': order.total_price,
                    'number_of_items': order.number_of_items,
                    'invoice': order.invoice,
                    'payment_method': order.payment_method,
                    'booking_date': order.booking_date.isoformat(),
                    'booking_status': order.booking_status,
                    'payment_status': order.payment_status,
                    'pickup_date_scheduled': order.pickup_date_scheduled.isoformat(),
                    'pickup_date_actual': order.pickup_date_actual.isoformat(),
                    'order_reference_code': order.order_reference_code,
                    'packed': order.packed,
                    # 'shipment_status': order.shipment_status,
                    # 'shipment_tracking_number': order.shipment_tracking_number,
                    # 'shipment_carrier': order.shipment_carrier,
                    # 'shipment_eta': order.shipment_eta.isoformat() if order.shipment_eta else None
                }
                user_data['orders'].append(order_data)

            # Extract user's storage units (if they exist)
            if hasattr(user, 'storage_units'):
                storage_units = user.storage_units
                for storage_unit in storage_units:
                    storage_unit_data = {
                        'id': storage_unit.id,
                        'name': storage_unit.name,
                        'description': storage_unit.description,
                        'size': storage_unit.size,
                        'capacity': storage_unit.capacity,
                        'price_per_month': storage_unit.price_per_month,
                        'available': storage_unit.available,
                        'address': storage_unit.address,
                        'latitude': storage_unit.latitude,
                        'longitude': storage_unit.longitude
                    }
                    user_data['storage_units'].append(storage_unit_data)

            user_list.append(user_data)

        # Return the user data list as JSON
        return jsonify({'users': user_list})

    except Exception as e:
        return jsonify({'error': str(e)})


# Route to get single user
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        # Find the user by user ID
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Create a user data dictionary
        user_data = {
            'user_id': user.user_id,
            'public_id': user.public_id,
            'full_name': user.full_name,
            'username': user.username,
            'email': user.email,
            'phone_number': user.phone_number,
            'profile_picture': user.profile_picture,
            'address': user.address,
            'role': user.role,
            'date_of_birth': user.date_of_birth.isoformat() if user.date_of_birth else None,
            'gender': user.gender,
            'bio': user.bio,
            'orders': [],
            'storage_units': []
        }

        # Extract user's orders
        orders = user.orders
        for order in orders:
            order_data = {
                'id': order.id,
                'order_date': order.order_date.isoformat(),
                'delivery_date': order.delivery_date.isoformat(),
                'total_price': order.total_price,
                'number_of_items': order.number_of_items,
                'invoice': order.invoice,
                'payment_method': order.payment_method,
                'booking_date': order.booking_date.isoformat(),
                'booking_status': order.booking_status,
                'payment_status': order.payment_status,
                'pickup_date_scheduled': order.pickup_date_scheduled.isoformat(),
                'pickup_date_actual': order.pickup_date_actual.isoformat(),
                'order_reference_code': order.order_reference_code,
                'packed': order.packed,
                'shipment_status': order.shipment_status,
                'shipment_tracking_number': order.shipment_tracking_number,
                'shipment_carrier': order.shipment_carrier,
                'shipment_eta': order.shipment_eta.isoformat() if order.shipment_eta else None
            }
            user_data['orders'].append(order_data)

        # Extract user's storage units (if they exist)
        if hasattr(user, 'storage_units'):
            storage_units = user.storage_units
            for storage_unit in storage_units:
                storage_unit_data = {
                    'id': storage_unit.id,
                    'name': storage_unit.name,
                    'description': storage_unit.description,
                    'size': storage_unit.size,
                    'capacity': storage_unit.capacity,
                    'price_per_month': storage_unit.price_per_month,
                    'available': storage_unit.available,
                    'address': storage_unit.address,
                    'latitude': storage_unit.latitude,
                    'longitude': storage_unit.longitude
                }
                user_data['storage_units'].append(storage_unit_data)

        # Return the user data as JSON
        return jsonify(user_data)

    except Exception as e:
        return jsonify({'error': str(e)})


#  Creating a user
@app.route('/user', methods=['POST'])
def create_user():
    try:
        data = request.get_json()

        # Check if required fields are provided in the request
        required_fields = ['username', 'email', 'password',
                           'full_name', 'phone_number', 'role']
        for field in required_fields:
            if field not in data:

                return jsonify({'error': f'Missing field: {field}'}), 400

        # Check if the username and email are already in use
        existing_user = User.query.filter_by(username=data['username']).first()
        existing_email = User.query.filter_by(email=data['email']).first()
        existing_phone = User.query.filter_by(
            phone_number=data['phone_number']).first()

        if existing_user:
            return jsonify({'error': 'Username is already taken'}), 409

        if existing_email:
            # Print the email that is already in use
            print(f"Email '{data['email']}' is already in use")
            return jsonify({'error': 'Email is already in use'}), 409

        if existing_phone:
            # Print the phone number that is already in use
            print(f"Phone number '{data['phone_number']}' is already in use")
            return jsonify({'error': 'Phone number is already in use'}), 409

        # Hash the password
        hashed_password = generate_password_hash(
            data['password'], method='pbkdf2:sha256')

        # Parse and convert the date_of_birth string to a Python date object
        date_of_birth_str = data.get('date_of_birth')
        date_of_birth = None

        if date_of_birth_str:
            try:
                date_of_birth = datetime.strptime(
                    date_of_birth_str, '%Y-%m-%d').date()
            except ValueError:
                # Handle invalid date format here, e.g., return an error response
                return jsonify({'error': 'Invalid date_of birth format. Please use YYYY-MM-DD'}), 400

        # Create a new user with all fields, including the date_of_birth
        new_user = User(
            public_id=str(uuid.uuid4()),
            username=data['username'],
            email=data['email'],
            full_name=data['full_name'],
            phone_number=data['phone_number'],
            password=hashed_password,
            role=data['role'],
            profile_picture=data.get('profile_picture'),
            address=data.get('address'),
            date_of_birth=date_of_birth,  # Use the parsed date_of_birth
            gender=data.get('gender'),
            bio=data.get('bio')
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'New user created!'})
    except Exception as e:
        # Print the exception for troubleshooting
        print("Exception:", e)

        db.session.rollback()
        return jsonify({'error': 'User creation failed. Please try again later.'}), 500


# Deleting a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
# @token_required
def delete_user(user_id):
    try:
        # Query the user by user_id
        user = User.query.get(user_id)

        if user is not None:
            # Delete the user from the database
            db.session.delete(user)
            db.session.commit()

            return jsonify({'message': 'User deleted successfully'})

        return jsonify({'message': 'User not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)})


# Updating a user details:
@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()

    # Retrieve the user from the database based on the user_id
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    try:
        if 'full_name' in data:
            user.full_name = data['full_name']

        if 'username' in data:
            # Check for a unique username
            existing_user = User.query.filter_by(
                username=data['username']).first()
            if existing_user and existing_user.user_id != user.user_id:
                return jsonify({'error': 'Username is already taken'}), 409
            user.username = data['username']

        if 'email' in data:
            # Check for a unique email
            existing_email = User.query.filter_by(email=data['email']).first()
            if existing_email and existing_email.user_id != user.user_id:
                return jsonify({'error': 'Email is already in use'}), 409
            user.email = data['email']

        if 'phone_number' in data:
            user.phone_number = data['phone_number']

        if 'role' in data:
            user.role = data['role']

        if 'profile_picture' in data:
            user.profile_picture = data['profile_picture']

        if 'address' in data:
            user.address = data['address']

        if 'bio' in data:
            user.bio = data['bio']

        if 'password' in data:
            # password hashed
            hashed_password = generate_password_hash(
                data['password'], method='pbkdf2:sha256')
            user.password = hashed_password

        if 'date_of_birth' in data:
            # Parse and convert the date_of_birth string to a Python date object
            date_of_birth_str = data['date_of_birth']
            date_of_birth = None

            if date_of_birth_str:
                try:
                    date_of_birth = datetime.strptime(
                        date_of_birth_str, '%Y-%m-%d').date()
                except ValueError:
                    # Handle invalid date format here, e.g., return an error response
                    return jsonify({'error': 'Invalid date of birth format. Please use YYYY-MM-DD'}), 400

            user.date_of_birth = date_of_birth

        if 'gender' in data:
            user.gender = data['gender']

        db.session.commit()

        updated_user_data = {
            'user_id': user.user_id,
            'full_name': user.full_name,
            'username': user.username,
            'email': user.email,
            'phone_number': user.phone_number,
            'role': user.role,
            'profile_picture': user.profile_picture,
            'address': user.address,
            'bio': user.bio,
            'date_of_birth': user.date_of_birth.strftime('%Y-%m-%d'),
            'gender': user.gender,
        }

        return jsonify({'message': 'User updated successfully', 'user': updated_user_data})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'User update failed. Please try again later.'}), 500


# Creating orders

# @app.route('/orders', methods=['POST'])
# def create_order():
#     try:
#         data = request.get_json()

#         print("Received Data:")
#         print(data)

#         # Validate the request data
#         required_fields = ['user_id', 'delivery_date', 'total_price', 'number_of_items', 'invoice', 'payment_method',
#                            'booking_date', 'booking_status', 'payment_status', 'pickup_date_scheduled', 'pickup_date_actual', 'order_reference_code']
#         for field in required_fields:
#             if field not in data:
#                 return jsonify({'error': f'Missing field: {field}'}), 400

#         # Extract relevant data from the request
#         user_id = data['user_id']
#         delivery_date = datetime.fromisoformat(data['delivery_date'])
#         total_price = data['total_price']
#         number_of_items = data['number_of_items']
#         invoice = data['invoice']
#         payment_method = data['payment_method']
#         booking_date = datetime.fromisoformat(data['booking_date'])
#         booking_status = data['booking_status']
#         payment_status = data['payment_status']
#         pickup_date_scheduled = datetime.fromisoformat(
#             data['pickup_date_scheduled'])
#         pickup_date_actual = datetime.fromisoformat(data['pickup_date_actual'])
#         order_reference_code = data['order_reference_code']

#         print("Processed Data:")
#         print("user_id:", user_id)
#         print("delivery_date:", delivery_date)
#         print("total_price:", total_price)
#         print("number_of_items:", number_of_items)
#         print("invoice:", invoice)
#         print("payment_method:", payment_method)
#         print("booking_date:", booking_date)
#         print("booking_status:", booking_status)
#         print("payment_status:", payment_status)
#         print("pickup_date_scheduled:", pickup_date_scheduled)
#         print("pickup_date_actual:", pickup_date_actual)
#         print("order_reference_code:", order_reference_code)

#         # Check if the user exists
#         user = User.query.get(user_id)
#         if not user:
#             print("User not found")
#             return jsonify({'error': 'User not found'}), 404

#         # Create a new order with the required parameters
#         new_order = Order(
#             user_id=user_id,
#             order_date=datetime.now(),
#             delivery_date=delivery_date,
#             total_price=total_price,
#             number_of_items=number_of_items,
#             invoice=invoice,
#             payment_method=payment_method,
#             booking_date=booking_date,
#             booking_status=booking_status,
#             payment_status=payment_status,
#             pickup_date_scheduled=pickup_date_scheduled,
#             pickup_date_actual=pickup_date_actual,
#             order_reference_code=order_reference_code,
#             packed=True
#         )

#         # Add the order to the database
#         db.session.add(new_order)
#         db.session.commit()

#         print("Order created successfully")
#         return jsonify({'message': 'Order created successfully', 'order_id': new_order.id}), 201

#     except Exception as e:
#         db.session.rollback()
#         print("Order creation failed:", str(e))
#         return jsonify({'error': 'Order creation failed. Please try again later.'}), 500

# @app.route('/orders', methods=['POST'])
# def create_order():
#     try:
#         data = request.get_json()

#         if not data:
#             print("Invalid JSON data in the request")
#             return jsonify({'error': 'Invalid JSON data in the request'}), 400

#         # Define a list of required fields
#         required_fields = [
#             'user_id',
#             'delivery_date',
#             'total_price',
#             'number_of_items',
#             'invoice',
#             'payment_method',
#             'booking_date',
#             'booking_status',
#             'payment_status',
#             'pickup_date_scheduled',
#             'pickup_date_actual',
#             'order_reference_code'
#         ]

#         # Check if all required fields are present
#         for field in required_fields:
#             if field not in data:
#                 print(f"Missing field: {field}")
#                 return jsonify({'error': f'Missing field: {field}'}), 400

#         # Validate and parse data
#         try:
#             user_id = int(data['user_id'])
#             # Parse the datetime strings into datetime objects
#             delivery_date = datetime.fromisoformat(data['delivery_date'])
#             total_price = float(data['total_price'])
#             number_of_items = int(data['number_of_items'])
#             invoice = data['invoice']
#             payment_method = data['payment_method']
#             booking_date = datetime.fromisoformat(data['booking_date'])
#             booking_status = data['booking_status']
#             payment_status = data['payment_status']
#             pickup_date_scheduled = datetime.fromisoformat(
#                 data['pickup_date_scheduled'])
#             pickup_date_actual = datetime.fromisoformat(
#                 data['pickup_date_actual'])
#             order_reference_code = data['order_reference_code']
#         except (ValueError, KeyError, TypeError):
#             print("Invalid data format in the request")
#             return jsonify({'error': 'Invalid data format in the request'}), 400

#         # Check if the user exists
#         user = User.query.get(user_id)
#         if not user:
#             print("User not found")
#             return jsonify({'error': 'User not found'}), 404

#         # Check for duplicate order reference code
#         if Order.query.filter_by(order_reference_code=order_reference_code).first():
#             print("Order with the same reference code already exists")
#             return jsonify({'error': 'Order with the same reference code already exists'}), 400

#         # Create a new order
#         new_order = Order(
#             user_id=user_id,
#             # order_date=datetime.utcnow(),  # Use datetime.utcnow() for order date
#             delivery_date=delivery_date,
#             total_price=total_price,
#             number_of_items=number_of_items,
#             invoice=invoice,
#             payment_method=payment_method,
#             booking_date=booking_date,
#             booking_status=booking_status,
#             payment_status=payment_status,
#             pickup_date_scheduled=pickup_date_scheduled,
#             pickup_date_actual=pickup_date_actual,
#             order_reference_code=order_reference_code,
#             packed=True,
#             pickup_status='pickup_address',
#             pickup_address='pickup_address'
#         )

#         # Add the order to the database
#         db.session.add(new_order)
#         db.session.commit()

#         print("Order created successfully")
#         return make_response(jsonify({'message': 'Order created successfully', 'order_id': new_order.id}), 201)

#     except Exception as e:
#         db.session.rollback()
#         print(f"Order creation failed: {str(e)}")
#         return jsonify({'error': 'Order creation failed. Please try again later.'}), 500

@app.route('/orders', methods=['POST'])
def create_order():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Invalid JSON data in the request'}), 400

        # Define a list of required fields
        required_fields = [
            'user_id',
            'delivery_date',
            'total_price',
            'number_of_items',
            'invoice',
            'payment_method',
            'booking_date',
            'booking_status',
            'payment_status',
            'pickup_date_scheduled',
            'pickup_date_actual',
            'order_reference_code'
        ]

        # Check if all required fields are present
        missing_fields = [
            field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

        # Parse and validate data
        try:
            user_id = int(data['user_id'])
            delivery_date = datetime.fromisoformat(data['delivery_date'])
            total_price = float(data['total_price'])
            number_of_items = int(data['number_of_items'])
            invoice = data.get('invoice')
            payment_method = data.get('payment_method', None)
            booking_date = datetime.fromisoformat(data['booking_date'])
            booking_status = data['booking_status']
            payment_status = data['payment_status']
            pickup_date_scheduled = datetime.fromisoformat(
                data['pickup_date_scheduled'])
            pickup_date_actual = datetime.fromisoformat(
                data['pickup_date_actual'])
            order_reference_code = data['order_reference_code']
        except (ValueError, KeyError, TypeError):
            return jsonify({'error': 'Invalid data format in the request'}), 400

        # Check if the user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Check for duplicate order reference code
        if Order.query.filter_by(order_reference_code=order_reference_code).first():
            return jsonify({'error': 'Order with the same reference code already exists'}), 400

        # Create a new order
        new_order = Order(
            user_id=user_id,
            delivery_date=delivery_date,
            total_price=total_price,
            number_of_items=number_of_items,
            invoice=invoice,
            payment_method=payment_method,
            booking_date=booking_date,
            booking_status=booking_status,
            payment_status=payment_status,
            pickup_date_scheduled=pickup_date_scheduled,
            pickup_date_actual=pickup_date_actual,
            order_reference_code=order_reference_code,
            packed=True,
            pickup_status='pickup_status',
            pickup_address='pickup_address'
        )

        # Add the order to the database
        db.session.add(new_order)
        db.session.commit()

        return make_response(jsonify({'message': 'Order created successfully', 'order_id': new_order.id}), 201)

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Order creation failed. Please try again later.'}), 500

# Getting all orders


@app.route('/orders', methods=['GET'])
def get_all_orders():
    try:
        # Retrieve all orders from the database
        orders = Order.query.all()

        # Create a list to store the order data
        order_list = []

        # Iterate through the orders and convert them to a dictionary
        for order in orders:
            order_data = {
                'order_id': order.id,
                'user_id': order.user_id,
                'order_date': order.order_date.isoformat(),
                'delivery_date': order.delivery_date.isoformat(),
                'total_price': order.total_price,
                'number_of_items': order.number_of_items,
                'invoice': order.invoice,
                'payment_method': order.payment_method,
                'booking_date': order.booking_date.isoformat(),
                'booking_status': order.booking_status,
                'payment_status': order.payment_status,
                'pickup_date_scheduled': order.pickup_date_scheduled.isoformat(),
                'pickup_date_actual': order.pickup_date_actual.isoformat(),
                'order_reference_code': order.order_reference_code,
                'packed': order.packed
            }
            order_list.append(order_data)

        # Return the list of orders as JSON
        return jsonify({'orders': order_list})

    except Exception as e:
        print("Failed to retrieve orders:", str(e))
        return jsonify({'error': 'Failed to retrieve orders'}), 500

# Getting a single order


@app.route('/orders/<int:order_id>', methods=['GET'])
def get_single_order(order_id):
    try:
        # Retrieve the order with the specified order_id from the database
        order = Order.query.get(order_id)

        if order is not None:
            # Convert the order data to a dictionary
            order_data = {
                'order_id': order.id,
                'user_id': order.user_id,
                'order_date': order.order_date.isoformat(),
                'delivery_date': order.delivery_date.isoformat(),
                'total_price': order.total_price,
                'number_of_items': order.number_of_items,
                'invoice': order.invoice,
                'payment_method': order.payment_method,
                'booking_date': order.booking_date.isoformat(),
                'booking_status': order.booking_status,
                'payment_status': order.payment_status,
                'pickup_date_scheduled': order.pickup_date_scheduled.isoformat(),
                'pickup_date_actual': order.pickup_date_actual.isoformat(),
                'order_reference_code': order.order_reference_code,
                'packed': order.packed
            }

            # Return the order data as JSON
            return jsonify(order_data)
        else:
            return jsonify({'error': 'Order not found'}), 404

    except Exception as e:
        print(f"Failed to retrieve order {order_id}: {str(e)}")
        return jsonify({'error': 'Failed to retrieve order'}), 500

# Updating order


@app.route('/order/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.get_json()

    # Retrieve the order from the database based on the order_id
    order = db.session.get(Order, order_id)  # Use Session.get()

    if not order:
        return jsonify({'error': 'Order not found'}), 404

    try:
        if 'delivery_date' in data:
            # Parse the string date into a datetime object
            order.delivery_date = datetime.strptime(
                data['delivery_date'], '%Y-%m-%d %H:%M:%S')

        if 'order_reference_code' in data:
            order.order_reference_code = data['order_reference_code']

        if 'invoice' in data:
            order.invoice = data['invoice']

        if 'payment_method' in data:
            order.payment_method = data['payment_method']

        if 'number_of_items' in data:
            order.number_of_items = data['number_of_items']

        if 'booking_date' in data:
            # Parse the string date into a datetime object
            order.booking_date = datetime.strptime(
                data['booking_date'], '%Y-%m-%d %H:%M:%S')

        if 'booking_status' in data:
            order.booking_status = data['booking_status']

        if 'total_price' in data:
            order.total_price = data['total_price']

        if 'payment_status' in data:
            order.payment_status = data['payment_status']

        if 'pickup_date_scheduled' in data:
            # Parse the string date into a datetime object
            order.pickup_date_scheduled = datetime.strptime(
                data['pickup_date_scheduled'], '%Y-%m-%d %H:%M:%S')

        if 'pickup_date_actual' in data:
            # Parse the string date into a datetime object
            order.pickup_date_actual = datetime.strptime(
                data['pickup_date_actual'], '%Y-%m-%d %H:%M:%S')

        if 'packed' in data:
            order.packed = data['packed']

        # Add other order attributes that you want to update

        db.session.commit()

        updated_order_data = {
            'id': order.id,
            'user_id': order.user_id,
            'delivery_date': order.delivery_date.strftime('%Y-%m-%d %H:%M:%S'),
            'order_reference_code': order.order_reference_code,
            'invoice': order.invoice,
            'payment_method': order.payment_method,
            'number_of_items': order.number_of_items,
            'booking_date': order.booking_date.strftime('%Y-%m-%d %H:%M:%S'),
            'booking_status': order.booking_status,
            'total_price': order.total_price,
            'payment_status': order.payment_status,
            'pickup_date_scheduled': order.pickup_date_scheduled.strftime('%Y-%m-%d %H:%M:%S'),
            'pickup_date_actual': order.pickup_date_actual.strftime('%Y-%m-%d %H:%M:%S'),
            'packed': order.packed,
        }

        print("Order updated successfully")

        return jsonify({'message': 'Order updated successfully', 'order': updated_order_data})
    except Exception as e:
        db.session.rollback()
        print(f"Order update failed. Error: {str(e)}")
        return jsonify({'error': 'Order update failed. Please try again later.'}), 500

# Deleting order


@app.route('/order/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    # Retrieve the order from the database based on the order_id
    order = db.session.get(Order, order_id)

    if not order:
        return jsonify({'error': 'Order not found'}), 404

    try:
        # Delete the order from the database
        db.session.delete(order)
        db.session.commit()

        return jsonify({'message': 'Order deleted successfully'})
    except Exception as e:
        db.session.rollback()
        print(f"Order deletion failed. Error: {str(e)}")
        return jsonify({'error': 'Order deletion failed. Please try again later.'}), 500
