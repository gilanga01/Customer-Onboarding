# Import the database object
from config import db

# Customer table mapped to MySQL
class Customer(db.Model):
    # Explicit table name in MySQL
    __tablename__ = 'customers'

    # Primary key column
    id = db.Column(db.Integer, primary_key=True)

    # Customer name (cannot be NULL)
    name = db.Column(db.String(100), nullable=False)

    # Customer email (cannot be NULL)
    email = db.Column(db.String(100), nullable=False)

    # Customer phone number
    phone = db.Column(db.String(20), nullable=False)

    # Convert database object to dictionary (for JSON response)
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone
        }
