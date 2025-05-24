from flask import Blueprint, request, jsonify
from datetime import datetime
from src.models.user import db
from src.models.customer import Customer

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'address', 'phone', 'installation_date']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'O campo {field} é obrigatório'}), 400
    
    # Validate installation date format
    try:
        installation_date = datetime.strptime(data['installation_date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Formato de data inválido. Use AAAA-MM-DD'}), 400
    
    # Get alert_days with default value if not provided
    alert_days = data.get('alert_days', 30)
    
    # Create new customer
    new_customer = Customer(
        name=data['name'],
        address=data['address'],
        phone=data['phone'],
        installation_date=installation_date,
        alert_days=alert_days
    )
    
    # Save to database
    try:
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({'message': 'Cliente criado com sucesso', 'customer': new_customer.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Falha ao criar cliente: {str(e)}'}), 500

@customer_bp.route('/customers', methods=['GET'])
def get_customers():
    # Get query parameters for filtering
    name_filter = request.args.get('name', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    
    # Start with base query
    query = Customer.query
    
    # Apply name filter if provided
    if name_filter:
        query = query.filter(Customer.name.ilike(f'%{name_filter}%'))
    
    # Apply date range filters if provided
    if start_date:
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            query = query.filter(Customer.installation_date >= start_date_obj)
        except ValueError:
            return jsonify({'error': 'Formato de data inicial inválido. Use AAAA-MM-DD'}), 400
    
    if end_date:
        try:
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(Customer.installation_date <= end_date_obj)
        except ValueError:
            return jsonify({'error': 'Formato de data final inválido. Use AAAA-MM-DD'}), 400
    
    # Execute query and return results
    customers = query.all()
    return jsonify({'customers': [customer.to_dict() for customer in customers]}), 200

@customer_bp.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Cliente não encontrado'}), 404
    return jsonify({'customer': customer.to_dict()}), 200

@customer_bp.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Cliente não encontrado'}), 404
    
    data = request.get_json()
    
    # Update fields if provided
    if 'name' in data and data['name']:
        customer.name = data['name']
    if 'address' in data and data['address']:
        customer.address = data['address']
    if 'phone' in data and data['phone']:
        customer.phone = data['phone']
    if 'installation_date' in data and data['installation_date']:
        try:
            customer.installation_date = datetime.strptime(data['installation_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Formato de data inválido. Use AAAA-MM-DD'}), 400
    if 'alert_days' in data:
        customer.alert_days = data['alert_days']
    
    # Save changes
    try:
        db.session.commit()
        return jsonify({'message': 'Cliente atualizado com sucesso', 'customer': customer.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Falha ao atualizar cliente: {str(e)}'}), 500

@customer_bp.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Cliente não encontrado'}), 404
    
    try:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'message': 'Cliente excluído com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Falha ao excluir cliente: {str(e)}'}), 500
