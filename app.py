# app.py
# -------------------------
# Main entry point of the application
# Initializes Flask, SQLAlchemy, JWT, and registers routes
# -------------------------

from flask import Flask
from config import db
from routes import routes
from flask_jwt_extended import JWTManager
from datetime import timedelta

# Create Flask app
app = Flask(__name__)

# -------------------------
# MySQL Configuration (XAMPP)
# -------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/onboarding_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# -------------------------
# JWT Configuration
# -------------------------
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Replace with env variable in production
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)

# -------------------------
# Register routes from routes.py
# -------------------------
app.register_blueprint(routes)

# -------------------------
# Run Flask application
# -------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
