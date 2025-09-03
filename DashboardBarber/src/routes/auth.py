import os
import jwt
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

auth_bp = Blueprint('auth', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Token inválido'}), 401
        
        if not token:
            return jsonify({'message': 'Token não fornecido'}), 401
        
        try:
            data = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS256'])
            current_user = data['username']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username') or data.get('email')
    password = data.get('password')
    
    if (username == os.getenv('ADMIN_USER') and 
        password == os.getenv('ADMIN_PASS')):
        
        token = jwt.encode({
            'role': 'admin',
            'username': username
        }, os.getenv('JWT_SECRET'), algorithm='HS256')
        
        user = {
            'id': '1',
            'email': username,
            'nome': 'Sr. Mendes'
        }
        
        return jsonify({'token': token, 'user': user})
    
    return jsonify({'message': 'Credenciais inválidas'}), 401

@auth_bp.route('/auth/verify', methods=['GET'])
@token_required
def verify_token(current_user):
    return jsonify({
        'valid': True,
        'user': {
            'id': '1',
            'email': current_user,
            'nome': 'Sr. Mendes'
        }
    })

