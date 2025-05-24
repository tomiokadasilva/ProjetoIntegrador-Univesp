from datetime import datetime, timedelta
from src.models.user import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    installation_date = db.Column(db.Date, nullable=False)
    alert_days = db.Column(db.Integer, default=30, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Customer {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'installation_date': self.installation_date.strftime('%Y-%m-%d'),
            'alert_days': self.alert_days,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def get_maintenance_date(self):
        """Calculate the next maintenance date (6 months after installation)"""
        return self.installation_date + timedelta(days=180)
    
    def is_maintenance_due(self, days_threshold=None):
        """Check if maintenance is due within the specified threshold days"""
        next_maintenance = self.get_maintenance_date()
        days_until_maintenance = (next_maintenance - datetime.now().date()).days
        
        # Use customer's specific alert_days if no threshold is provided
        if days_threshold is None:
            days_threshold = self.alert_days
            
        return days_until_maintenance <= days_threshold
