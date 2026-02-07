# routes.py
# -------------------------
# Contains all API routes (CRUD) and JWT authentication
# -------------------------

from flask import Blueprint, request, jsonify
from config import db
from models import Customer
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# Create Blueprint
routes = Blueprint('routes', __name__)

# -------------------------
# Hardcoded user for demonstration
# -------------------------
USERS = {
    "admin": "password123"
}

# -------------------------
# LOGIN - generate JWT token
# POST /login
# -------------------------
@routes.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return {"error": "Missing username or password"}, 400

    if USERS.get(username) != password:
        return {"error": "Invalid credentials"}, 401

    token = create_access_token(identity=username)
    return {"token": token}, 200

# -------------------------
# HOME route (no auth)
# -------------------------
@routes.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Welcome to the Customer Onboarding API!"}), 200

# -------------------------
# CREATE customer
# POST /onboard
# -------------------------
@routes.route('/onboard', methods=['POST'])
@jwt_required()
def onboard_customer():
    data = request.json
    required_fields = ['name', 'email', 'phone']

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing {field} field"}), 400

    customer = Customer(
        name=data['name'],
        email=data['email'],
        phone=data['phone']
    )

    db.session.add(customer)
    db.session.commit()

    return jsonify({"message": "Customer created", "data": customer.to_dict()}), 201

# -------------------------
# READ all customers
# GET /onboarding
# -------------------------
@routes.route('/onboarding', methods=['GET'])
@jwt_required()
def get_all_customers():
    customers = Customer.query.all()
    return jsonify([c.to_dict() for c in customers]), 200

# -------------------------
# READ one customer by ID
# GET /onboarding/<id>
# -------------------------
@routes.route('/onboarding/<int:id>', methods=['GET'])
@jwt_required()
def get_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    return jsonify(customer.to_dict()), 200

# -------------------------
# UPDATE customer
# PUT /onboarding/<id>
# -------------------------
@routes.route('/onboarding/<int:id>', methods=['PUT'])
@jwt_required()
def update_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    data = request.json
    customer.name = data.get('name', customer.name)
    customer.email = data.get('email', customer.email)
    customer.phone = data.get('phone', customer.phone)

    db.session.commit()

    return jsonify({"message": "Customer updated", "data": customer.to_dict()}), 200

# -------------------------
# DELETE customer
# DELETE /onboarding/<id>
# -------------------------
@routes.route('/onboarding/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted successfully"}), 200
