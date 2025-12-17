import pandas as pd
from prophet import Prophet
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/inflation_history.csv')

def get_forecast_for_category(df, category, months=60):
    # Filter and setup for Prophet (ds, y)
    cat_df = df[df['category'] == category].copy()
    cat_df = cat_df.rename(columns={'date': 'ds', 'rate': 'y'})
    cat_df['ds'] = pd.to_datetime(cat_df['ds'])
    
    # Train
    m = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
    m.fit(cat_df)
    
    # Predict
    future = m.make_future_dataframe(periods=months, freq='MS')
    forecast = m.predict(future)
    
    # Extract results
    # Past 24 months + Future
    total_len = len(forecast)
    # We want valid history + future. 
    # Let's return the tail(24 + months) generally
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(24 + months).to_dict('records')

def generate_inflation_forecast(months=60):
    if not os.path.exists(DATA_PATH):
        return {"error": "Dataset not found"}
        
    df = pd.read_csv(DATA_PATH)
    
    results = {}
    categories = ['Food', 'Fuel', 'Healthcare']
    
    for cat in categories:
        forecast_data = get_forecast_for_category(df, cat, months)
        results[cat] = forecast_data
        
    return results

def get_latest_rates():
    if not os.path.exists(DATA_PATH):
        return {"Food": 0.08, "Fuel": 0.06, "Healthcare": 0.10} # Fallback
        
    df = pd.read_csv(DATA_PATH)
    latest_rates = {}
    for cat in ['Food', 'Fuel', 'Healthcare']:
        # Get last recorded rate
        val = df[df['category'] == cat].iloc[-1]['rate']
        latest_rates[cat] = val / 100.0 # Convert 8.0 to 0.08
    return latest_rates
