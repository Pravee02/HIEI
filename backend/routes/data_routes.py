from flask import Blueprint, jsonify, request
from models import db, User, PolicyMaker, UserFinancials, CallbackRequest
from datetime import datetime

data_bp = Blueprint('data', __name__)

# --- User: Save Calculator Results ---
@data_bp.route('/spending', methods=['POST'])
def save_spending():
    data = request.json
    try:
        new_record = UserFinancials(
            user_id=data['user_id'],
            salary=data.get('salary', 0),
            food_spend=data.get('food', 0),
            fuel_spend=data.get('fuel', 0),
            health_spend=data.get('health', 0),
            extra_spend=data.get('extra_spend', 0),
            total_spend=data.get('total_spend', 0),
            future_total_spend=data.get('future_total_spend', 0),
            salary_status=data.get('salary_status', 'Unknown'),
            most_affected_category=data.get('most_affected_category', 'Stable')
        )
        db.session.add(new_record)
        db.session.commit()
        return jsonify({"message": "Financial data saved successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- User: View available policy makers ---
@data_bp.route('/policy-makers', methods=['GET'])
def get_policy_makers():
    pms = PolicyMaker.query.all()
    result = [{
        "username": pm.username,
        "phone": pm.phone,
        "policy_area": pm.policy_area
    } for pm in pms]
    return jsonify(result)

# --- User: Get own history ---
@data_bp.route('/history/<int:user_id>', methods=['GET'])
def get_user_history(user_id):
    history = UserFinancials.query.filter_by(user_id=user_id).order_by(UserFinancials.created_at.desc()).all()
    result = [{
        "date": r.created_at.strftime("%Y-%m-%d"),
        "total_spend": r.total_spend,
        "future_total_spend": r.future_total_spend,
        "salary_status": r.salary_status,
        "most_affected": r.most_affected_category
    } for r in history]
    return jsonify(result)

# --- Callback Request ---
@data_bp.route('/callback', methods=['POST'])
def save_callback():
    data = request.json
    try:
        new_cb = CallbackRequest(
            user_id=data['user_id'],
            insurer_name=data['insurer_name']
        )
        db.session.add(new_cb)
        db.session.commit()
        return jsonify({"message": "Callback requested"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Policy Maker: Get all users and their latest stats ---
@data_bp.route('/users-insights', methods=['GET'])
def get_users_insights():
    try:
        users = User.query.all()
        result = []
        
        for u in users:
            # Find the MOST RECENT financial submission for this user
            latest = UserFinancials.query.filter_by(user_id=u.id).order_by(UserFinancials.created_at.desc()).first()
            
            financial_data = None
            if latest:
                financial_data = {
                    "salary": latest.salary,
                    "total_spend": latest.total_spend,
                    "future_total_spend": latest.future_total_spend,
                    "salary_status": latest.salary_status,
                    "most_affected_category": latest.most_affected_category
                }
            
            # Format row
            result.append({
                "id": u.id,
                "username": u.username,
                "phone": u.phone or "Not Provided",
                "household_group": u.household_group or "Not Provided",
                "financials": financial_data # Can be None if no data
            })
        
        return jsonify(result)
    except Exception as e:
        print(f"Error fetching insights: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
