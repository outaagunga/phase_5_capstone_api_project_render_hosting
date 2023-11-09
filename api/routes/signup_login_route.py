
from flask import flash, jsonify, redirect, render_template, request, session
from models.main import app, db
from models.user import User


# Signup route


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Perform data validation (e.g., check for duplicate usernames or emails)
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)).first()
        if existing_user:
            flash(
                'Username or email already exists. Please choose a different one.', 'danger')
            return jsonify({'error': 'Username or email already exists'})

        # Create a new user and add it to the database
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. You can now log in.', 'success')
        # Return the user object as JSON
        return jsonify({'user': new_user.to_dict()})

    # Handle GET requests here
    return render_template('signup.html')

# Login riute


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            # Log the user in by storing their user ID in the session
            session['user_id'] = user.user_id
            flash('Login successful.', 'success')
            return redirect('/dashboard')
        else:
            error_message = 'Login failed. Please check your username and password.'
            # Return the error message and user object as JSON
            return jsonify({'error': error_message, 'user': None}), 401

    # Return an error message if the request method is not POST
    error_message = 'Invalid request method.'
    return jsonify({'error': error_message, 'user': None}), 400


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
