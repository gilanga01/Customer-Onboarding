# Blueprint allows splitting routes into files
from flask import Blueprint, request, jsonify

# Import database session
from config import db

# Import Customer model
from models import Customer

# Create a Blueprint for routes
routes = Blueprint('routes', __name__)

# ---------------------------
# Home Route
# ---------------------------
@routes.route('/', methods=['GET'])
def index():
    # Simple test endpoint
    return jsonify({
        "message": "Welcome to the Customer Onboarding API!"
    }), 200


# ---------------------------
# Create Customer (POST)
# ---------------------------
@routes.route('/onboard', methods=['POST'])
def onboard_customer():
    # Read JSON data from request
    data = request.json

    # Required fields validation
    required_fields = ['name', 'email', 'phone']
    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"Missing {field} field"
            }), 400

    # Create new Customer object
    customer = Customer(
        name=data['name'],
        email=data['email'],
        phone=data['phone']
    )

    # Save customer to database
    db.session.add(customer)
    db.session.commit()

    # Return success response
    return jsonify({
        "message": "Customer onboarded successfully!",
        "data": customer.to_dict()
    }), 201


# ---------------------------
# Get All Customers (GET)
# ---------------------------
@routes.route('/onboarding', methods=['GET'])
def get_onboarding_data():
    # Query all customers from database
    customers = Customer.query.all()

    # Convert list of objects to list of dictionaries
    return jsonify([
        customer.to_dict() for customer in customers
    ]), 200
