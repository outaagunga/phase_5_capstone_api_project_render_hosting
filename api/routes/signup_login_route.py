
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

    # Perform data validation (e.g., check for duplicate usernames or emails)
    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)).first()

    if existing_user:
        error_message = 'Username or email already exists. Please choose a different one.'
        return jsonify({'error': error_message}), 400

    # Hash the password before storing it
    hashed_password = generate_password_hash(password, method='sha256')

    # Create a new user and add it to the database
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)

    try:
        db.session.commit()
    except Exception as e:
        error_message = 'An error occurred while creating your account. Please try again later.'
        return jsonify({'error': error_message}), 500

    success_message = 'Registration successful. You can now log in.'
    return jsonify({'message': success_message})

# Handle GET requests here


@app.route('/signup', methods=['GET'])
def render_signup_page():
    return render_template('signup.html')

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         email = request.form.get('email')
#         password = request.form.get('password')

#         # Perform data validation (e.g., check for duplicate usernames or emails)
#         existing_user = User.query.filter(
#             (User.username == username) | (User.email == email)).first()
#         if existing_user:
#             flash(
#                 'Username or email already exists. Please choose a different one.', 'danger')
#             return jsonify({'error': 'Username or email already exists'})

#         # Create a new user and add it to the database
#         new_user = User(username=username, email=email, password=password)
#         db.session.add(new_user)
#         db.session.commit()
#         flash('Registration successful. You can now log in.', 'success')
#         # Return the user object as JSON
#         return jsonify({'user': new_user.to_dict()})

#     # Handle GET requests here
#     return render_template('signup.html')

# Login riute


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        # Check the hashed password
        if user and check_password_hash(user.password, password):
            # Log the user in by storing their user ID in the session
            session['user_id'] = user.user_id
            success_message = 'Login successful.'
            # Return the success message and user object as JSON
            return jsonify({'message': success_message, 'user': user.to_dict()}), 200
        else:
            error_message = 'Login failed. Please check your username and password.'
            # Return the error message and user object as JSON
            return jsonify({'error': error_message, 'user': None}), 401

    # Return an error message if the request method is not POST
    error_message = 'Invalid request method.'
    return jsonify({'error': error_message, 'user': None}), 400


# @app.route('/login', methods=['POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')

#         user = User.query.filter_by(username=username).first()
#         if user and user.check_password(password):
#             # Log the user in by storing their user ID in the session
#             session['user_id'] = user.user_id
#             flash('Login successful.', 'success')
#             return redirect('/dashboard')
#         else:
#             error_message = 'Login failed. Please check your username and password.'
#             # Return the error message and user object as JSON
#             return jsonify({'error': error_message, 'user': None}), 401

#     # Return an error message if the request method is not POST
#     error_message = 'Invalid request method.'
#     return jsonify({'error': error_message, 'user': None}), 400


# Logout

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.', 'success')
    return redirect('/login')


# # Login
# @app.route('/login', methods=['POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')

#         user = User.query.filter_by(username=username).first()
#         if user and user.check_password(password):
#             # Log the user in by storing their user ID in the session
#             session['user_id'] = user.user_id
#             flash('Login successful.', 'success')
#             return redirect('/dashboard')
#         else:
#             flash('Login failed. Please check your username and password.', 'danger')

#     return render_template('login.html')


# # @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         email = request.form.get('email')
#         password = request.form.get('password')

#         # Perform data validation (e.g., check for duplicate usernames or email)

#         # Create a new user and add it to the database
#         new_user = User(username=username, email=email, password=password)
#         db.session.add(new_user)
#         db.session.commit()
#         flash('Registration successful. You can now log in.', 'success')
#         return redirect('/login')

#     return render_template('signup.html')


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')

#         user = User.query.filter_by(username=username).first()
#         if user and user.check_password(password):
#             # Log the user in by storing their user ID in the session
#             session['user_id'] = user.user_id
#             flash('Login successful.', 'success')
#             return redirect('/dashboard')
#         else:
#             flash('Login failed. Please check your username and password.', 'danger')

#     return render_template('login.html')


# signup


# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         email = request.form.get('email')
#         password = request.form.get('password')

#         # Perform data validation (e.g., check for duplicate usernames or emails)
#         existing_user = User.query.filter(
#             (User.username == username) | (User.email == email)).first()
#         if existing_user:
#             flash(
#                 'Username or email already exists. Please choose a different one.', 'danger')
#             return redirect('/signup')

#         # Create a new user and add it to the database
#         new_user = User(username=username, email=email, password=password)
#         db.session.add(new_user)
#         db.session.commit()
#         flash('Registration successful. You can now log in.', 'success')
#         return redirect('/login')

#     return render_template('signup.html')


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
