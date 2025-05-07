from flask import Blueprint, request,request, jsonify
from app.models import User, db
from flask_jwt_extended import create_access_token
import datetime

bp = Blueprint('auth', __name__)

#registering an endpoint
@bp.route('/register', methods = ['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing email or password'}), 400
    
    if User.query.filter_by(email = data['email']).first():
        return jsonify({'Error': 'User already exists'}), 400
    
    new_user = User(email = data['email'])
    new_user.set_password(data['password'])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


#login endpoint
@bp.route('/login', methods = ['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email = data.get('email')).first()

    if user and user.check_password(password = data.get('password')):
        token =  create_access_token(
            identity=user.id,
            expires_delta=datetime.timedelta(days=1)

        )

        return jsonify(access_token= token), 200
    
    return jsonify({"error": "Invalid credentials"}), 401
    