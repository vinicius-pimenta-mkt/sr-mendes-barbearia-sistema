import os
import jwt
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

load_dotenv()

auth_bp = Blueprint('auth', __name__)

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

