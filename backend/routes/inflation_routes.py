from flask import Blueprint, jsonify
from services.forecasting import generate_inflation_forecast, get_latest_rates

inflation_bp = Blueprint('inflation', __name__)

@inflation_bp.route('/forecast', methods=['GET'])
def get_forecast():
    forecast = generate_inflation_forecast(months=60)
    return jsonify(forecast)

@inflation_bp.route('/rates', methods=['GET'])
def get_rates():
    # Return latest known rates
    # Ideally, for calculator, we might want the average rate over the next N months, 
    # but initially we'll return the base rates that the calculator asks for.
    return jsonify(get_latest_rates())
