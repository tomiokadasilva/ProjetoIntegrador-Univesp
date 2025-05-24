from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from src.models.customer import Customer

alert_bp = Blueprint('alert', __name__)

@alert_bp.route('/alerts', methods=['GET'])
def get_maintenance_alerts():
    # Get query parameters for filtering
    days_threshold = request.args.get('days_threshold', 30, type=int)
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    
    # Calculate the date range for maintenance alerts
    today = datetime.now().date()
    
    # Start with all customers
    customers = Customer.query.all()
    
    # Filter alerts based on maintenance dates
    alerts = []
    for customer in customers:
        maintenance_date = customer.get_maintenance_date()
        
        # Apply date range filters if provided
        if start_date:
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
                if maintenance_date < start_date_obj:
                    continue
            except ValueError:
                return jsonify({'error': 'Invalid start_date format. Use YYYY-MM-DD'}), 400
        
        if end_date:
            try:
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
                if maintenance_date > end_date_obj:
                    continue
            except ValueError:
                return jsonify({'error': 'Invalid end_date format. Use YYYY-MM-DD'}), 400
        
        # Calculate days until maintenance
        days_until_maintenance = (maintenance_date - today).days
        
        # Only include alerts within the threshold
        if days_until_maintenance <= days_threshold:
            alerts.append({
                'customer_id': customer.id,
                'customer_name': customer.name,
                'customer_phone': customer.phone,
                'installation_date': customer.installation_date.strftime('%Y-%m-%d'),
                'maintenance_date': maintenance_date.strftime('%Y-%m-%d'),
                'days_until_maintenance': days_until_maintenance,
                'status': 'Overdue' if days_until_maintenance < 0 else 'Due Soon'
            })
    
    # Sort alerts by days_until_maintenance (most urgent first)
    alerts.sort(key=lambda x: x['days_until_maintenance'])
    
    return jsonify({
        'alerts': alerts,
        'total_alerts': len(alerts),
        'overdue_alerts': sum(1 for alert in alerts if alert['days_until_maintenance'] < 0)
    }), 200

@alert_bp.route('/alerts/summary', methods=['GET'])
def get_alerts_summary():
    # Get all customers
    customers = Customer.query.all()
    
    today = datetime.now().date()
    
    # Calculate summary statistics
    total_customers = len(customers)
    maintenance_due_7days = 0
    maintenance_due_30days = 0
    maintenance_overdue = 0
    
    for customer in customers:
        maintenance_date = customer.get_maintenance_date()
        days_until_maintenance = (maintenance_date - today).days
        
        if days_until_maintenance < 0:
            maintenance_overdue += 1
        elif days_until_maintenance <= 7:
            maintenance_due_7days += 1
        elif days_until_maintenance <= 30:
            maintenance_due_30days += 1
    
    return jsonify({
        'total_customers': total_customers,
        'maintenance_due_7days': maintenance_due_7days,
        'maintenance_due_30days': maintenance_due_30days,
        'maintenance_overdue': maintenance_overdue
    }), 200
