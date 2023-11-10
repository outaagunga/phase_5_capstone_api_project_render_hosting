
from flask import flash, jsonify, redirect, render_template, request, session
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from models.main import app, db
from models.user import User


# Signup route

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    if password is None:
        return jsonify({'error': 'Password is missing in the request'}), 400

    # Perform data validation (e.g., check for duplicate usernames or emails)
    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)).first()

    if existing_user:
        error_message = 'Username or email already exists. Please choose a different one.'
        return jsonify({'error': error_message}), 400

    # Hash the password using 'pbkdf2:sha256' before storing it
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    # Create a new user and add it to the database
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)

    try:
        db.session.commit()
    except Exception as e:
        error_message = 'An error occurred while creating your account. Please try again later.'
        return jsonify({'error': error_message}), 500

    success_message = 'Registration successful. You can now log in.'
    # Add this print statement
    print("User successfully registered:", username)
    return jsonify({'message': success_message})

# Handle GET requests here


@app.route('/signup', methods=['GET'])
def render_signup_page():
    return render_template('signup.html')

# Login Route (GET)


@app.route('/login', methods=['GET'])
def render_login_page():
    return render_template('login.html')


# # Login route
# Login route
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    print("Received username:", username)
    print("Received password:", password)

    if username is None or password is None:
        print("Username or password is missing in the request")
        return jsonify({'error': 'Username or password is missing in the request'}), 400

    # Query the database to find the user by their username
    user = User.query.filter_by(username=username).first()

    if user is None:
        print("User not found")
        return jsonify({'error': 'User not found'}), 404

    # Check if the provided password matches the stored hashed password
    if not check_password_hash(user.password, password):
        print("Invalid password")
        return jsonify({'error': 'Invalid password'}), 401

    # Successful login
    success_message = 'Login successful. Welcome, {}!'.format(user.username)
    print("Successful login for user:", user.username)
    return jsonify({'message': success_message})


# Logout


@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id')
        flash('Logged out successfully.', 'success')
        return jsonify({'message': 'Logged out successfully'}), 200
    else:
        return jsonify({'error': 'You are not logged in.'}), 401


# # Login form

# <form method="POST" action="/login">
#     <input type="text" name="username" placeholder="Username" required>
#     <input type="password" name="password" placeholder="Password" required>
#     <input type="submit" value="Log In">
# </form>


# signup form
# <form method="POST" action="/signup">
#     <input type="text" name="username" placeholder="Username" required>
#     <input type="email" name="email" placeholder="Email" required>
#     <input type="password" name="password" placeholder="Password" required>
#     <input type="submit" value="Sign Up">
# </form>
