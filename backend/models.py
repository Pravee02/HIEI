from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# User Model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False) # Maps to 'name' in prompt
    phone = db.Column(db.String(20), nullable=True)
    password_hash = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    household_group = db.Column(db.String(50), nullable=True) # Added for persistence
    
    # Relationship to spending
    financials = db.relationship('UserFinancials', backref='user', lazy=True)

# Policy Maker Model
class PolicyMaker(db.Model):
    __tablename__ = 'policymakers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False) # Name
    phone = db.Column(db.String(20), nullable=True)
    password_hash = db.Column(db.String(120), nullable=False)
    policy_area = db.Column(db.String(100), nullable=True)

# User Financials Model (Replaces Spending)
class UserFinancials(db.Model):
    __tablename__ = 'user_financials'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Financial Inputs
    salary = db.Column(db.Float, nullable=False, default=0.0)
    food_spend = db.Column(db.Float, nullable=False, default=0.0)
    fuel_spend = db.Column(db.Float, nullable=False, default=0.0)
    health_spend = db.Column(db.Float, nullable=False, default=0.0)
    extra_spend = db.Column(db.Float, nullable=False, default=0.0) # Fixed expenses/EMI
    
    # Calculated Metrics
    total_spend = db.Column(db.Float, nullable=False, default=0.0) # Current total
    future_total_spend = db.Column(db.Float, nullable=False, default=0.0) # Predicted total
    salary_status = db.Column(db.String(20), default="SURPLUS") # SURPLUS / DEFICIT
    most_affected_category = db.Column(db.String(50), default="Stable")
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Inflation Data Model (kept for potential extensions, but we will use CSV for main logic)
class InflationData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    rate = db.Column(db.Float, nullable=False)
# Callback Request Model (Insurance Inquiries)
class CallbackRequest(db.Model):
    __tablename__ = 'callback_requests'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    insurer_name = db.Column(db.String(100), nullable=True) # or policy type
    status = db.Column(db.String(20), default='Pending') # Pending, Contacted
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
