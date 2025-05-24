from flask import Blueprint, jsonify, request, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
from src.models.user import User, db

user_bp = Blueprint('user', __name__)

# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check if token is in headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'error': 'Token de autenticação ausente!'}), 401
        
        try:
            # Decode token
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
            
            if not current_user:
                return jsonify({'error': 'Token de autenticação inválido!'}), 401
                
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token de autenticação expirado!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token de autenticação inválido!'}), 401
            
        return f(current_user, *args, **kwargs)
    
    return decorated

@user_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'O campo {field} é obrigatório'}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Nome de usuário já existe'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email já existe'}), 400
    
    # Create new user
    new_user = User(
        username=data['username'],
        email=data['email']
    )
    new_user.set_password(data['password'])
    
    # Set as admin if it's the first user
    if User.query.count() == 0:
        new_user.is_admin = True
    
    # Save to database
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            'message': 'Usuário cadastrado com sucesso',
            'user': new_user.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Falha ao cadastrar usuário: {str(e)}'}), 500

@user_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Validate required fields
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Usuário e senha são obrigatórios'}), 400
    
    # Find user
    user = User.query.filter_by(username=data['username']).first()
    
    # Check if user exists and password is correct
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Usuário ou senha inválidos'}), 401
    
    # Generate token
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, current_app.config['SECRET_KEY'], algorithm="HS256")
    
    return jsonify({
        'message': 'Login realizado com sucesso',
        'token': token,
        'user': user.to_dict(),
        'expires_in': 86400  # 24 hours in seconds
    }), 200

@user_bp.route('/auth/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    return jsonify({
        'user': current_user.to_dict()
    }), 200

@user_bp.route('/users', methods=['GET'])
@token_required
def get_users(current_user):
    # Only admin can view all users
    if not current_user.is_admin:
        return jsonify({'error': 'Acesso não autorizado'}), 403
        
    users = User.query.all()
    return jsonify({'users': [user.to_dict() for user in users]}), 200

@user_bp.route('/users/<int:user_id>', methods=['GET'])
@token_required
def get_user(current_user, user_id):
    # Users can only view their own profile unless they're admin
    if user_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Acesso não autorizado'}), 403
        
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
        
    return jsonify({'user': user.to_dict()}), 200

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user(current_user, user_id):
    # Users can only update their own profile unless they're admin
    if user_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Acesso não autorizado'}), 403
        
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    data = request.get_json()
    
    # Update fields if provided
    if 'username' in data and data['username']:
        # Check if username is already taken by another user
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({'error': 'Nome de usuário já existe'}), 400
        user.username = data['username']
        
    if 'email' in data and data['email']:
        # Check if email is already taken by another user
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({'error': 'Email já existe'}), 400
        user.email = data['email']
        
    if 'password' in data and data['password']:
        user.set_password(data['password'])
    
    # Only admin can change admin status
    if 'is_admin' in data and current_user.is_admin:
        user.is_admin = bool(data['is_admin'])
    
    # Save changes
    try:
        db.session.commit()
        return jsonify({'message': 'Usuário atualizado com sucesso', 'user': user.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Falha ao atualizar usuário: {str(e)}'}), 500

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, user_id):
    # Only admin can delete users, and users can delete themselves
    if user_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Acesso não autorizado'}), 403
        
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    # Prevent deleting the last admin
    if user.is_admin and User.query.filter_by(is_admin=True).count() <= 1:
        return jsonify({'error': 'Não é possível excluir o último usuário administrador'}), 400
    
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Usuário excluído com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Falha ao excluir usuário: {str(e)}'}), 500
