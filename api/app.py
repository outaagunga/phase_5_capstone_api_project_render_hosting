# app.py
from flask import jsonify, request

from flask import request, jsonify, make_response, session
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
from models.main import app
from routes.deliveries_route import *
from routes.transactions_route import *
from routes.inventory_route import *
from routes.pickups_route import *
from routes.receipts_route import *
from routes.shippings_route import *
from routes.stored_items_route import *
from routes.warehouse_route import *
from routes.user_route import *


from models.user import User

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0')
