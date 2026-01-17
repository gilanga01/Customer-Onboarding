from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for onboarding details
onboarding_data = []

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Welcome to the Customer Onboarding API!"}), 200

@app.route('/onboard', methods=['POST'])
def onboard_customer():
    # Get data from request
    data = request.json

    # Validate input
    required_fields = ['name', 'email', 'phone']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing {field} field'}), 400

    # Add to onboarding data
    onboarding_data.append(data)
    
    return jsonify({'message': 'Customer onboarded successfully!', 'data': data}), 201

@app.route('/onboarding', methods=['GET'])
def get_onboarding_data():
    return jsonify(onboarding_data), 200

if __name__ == '__main__':
    app.run(debug=True)