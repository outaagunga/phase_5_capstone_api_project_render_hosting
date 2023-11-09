# from models.main import app, db
# from models.user import User
# from werkzeug.security import generate_password_hash

# # Create a function to simulate user registration


# def simulate_signup(username, email, password):
#     with app.test_request_context(method='POST', data={
#         'username': username,
#         'email': email,
#         'password': password
#     }):
#         # Perform data validation
#         existing_user = User.query.filter(
#             (User.username == username) | (User.email == email)).first()

#         if existing_user:
#             error_message = 'Username or email already exists. Please choose a different one.'
#             return {'error': error_message}, 400

#         # Hash the password before storing it
#         hashed_password = generate_password_hash(password, method='sha256')

#         # Create a new user and add it to the database
#         new_user = User(username=username, email=email,
#                         password=hashed_password)
#         db.session.add(new_user)

#         try:
#             db.session.commit()
#         except Exception as e:
#             error_message = 'An error occurred while creating your account. Please try again later.'
#             return {'error': error_message}, 500

#         success_message = 'Registration successful. You can now log in.'
#         return {'message': success_message}


# # Test user registration
# result = simulate_signup('testuser', 'testuser@example.com', 'testpassword')
# print(result)
