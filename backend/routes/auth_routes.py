from flask import Blueprint, jsonify, request
from models import db, User, PolicyMaker

auth_bp = Blueprint('auth', __name__)

# --- User Auth ---
@auth_bp.route('/login/user', methods=['POST'])
def login_user():
    data = request.json
    user = User.query.filter_by(username=data.get('username')).first()
    # Simple password check for demo (use hash in prod)
    if user and user.password_hash == data.get('password'): 
        return jsonify({
            "token": f"user-{user.id}", 
            "role": "user",
            "user_id": user.id,
            "username": user.username,
            "phone": user.phone
        })
    return jsonify({"error": "Invalid User credentials"}), 401

@auth_bp.route('/register/user', methods=['POST'])
def register_user():
    data = request.json
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({"error": "User already exists"}), 400
    
    new_user = User(
        username=data.get('username'),
        password_hash=data.get('password'), 
        phone=data.get('phone'),
        address=data.get('address'),
        household_group=data.get('household_group')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

# --- Policy Maker Auth ---
@auth_bp.route('/login/policy', methods=['POST'])
def login_policy_maker():
    data = request.json
    pm = PolicyMaker.query.filter_by(username=data.get('username')).first()
    if pm and pm.password_hash == data.get('password'):
        return jsonify({
            "token": f"pm-{pm.id}", 
            "role": "policy_maker",
            "pm_id": pm.id,
            "username": pm.username,
            "policy_area": pm.policy_area
        })
    return jsonify({"error": "Invalid Policy Maker credentials"}), 401

@auth_bp.route('/register/policy', methods=['POST'])
def register_policy_maker():
    data = request.json
    if PolicyMaker.query.filter_by(username=data.get('username')).first():
        return jsonify({"error": "Policy Maker already exists"}), 400
    
    new_pm = PolicyMaker(
        username=data.get('username'),
        password_hash=data.get('password'),
        phone=data.get('phone'),
        policy_area=data.get('policy_area')
    )
    db.session.add(new_pm)
    db.session.commit()
    return jsonify({"message": "Policy Maker registered successfully"}), 201
