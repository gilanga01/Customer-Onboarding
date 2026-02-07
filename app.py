# Import Flask
from flask import Flask

# Import database object
from config import db

# Import routes blueprint
from routes import routes

# Create Flask application instance
app = Flask(__name__)

# ---------------------------
# MySQL Configuration (XAMPP)
# ---------------------------
# Default XAMPP credentials:
# user: root
# password: (empty)
# host: localhost
# database: onboarding_db

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/onboarding_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database with Flask app
db.init_app(app)

# Register routes with the app
app.register_blueprint(routes)

# ---------------------------
# Run Application
# ---------------------------
if __name__ == '__main__':
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    # Start Flask development server
    app.run(debug=True)
