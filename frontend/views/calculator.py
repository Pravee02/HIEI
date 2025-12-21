import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime

from utils.api import API_URL

API_BASE = f"{API_URL}/api"

def display_calculator():
    st.header("Inflation Calculator & Planner")
    
    # 1. Inputs
    col1, col2 = st.columns(2)
    with col1:
        salary = st.number_input("Monthly Salary (₹)", min_value=0.0, value=50000.0)
        extra_fixed = st.number_input("EMI / Other Fixed Spending", min_value=0.0, value=15000.0)
        group = st.selectbox("Household Group", ["Urban Poor", "Urban Rich", "Rural Poor", "Rural Rich"])
        
    with col2:
        food_spend = st.number_input("Food Spending (₹)", min_value=0.0, value=8000.0)
        fuel_spend = st.number_input("Fuel/Transport Spending (₹)", min_value=0.0, value=3000.0)
        health_spend = st.number_input("Healthcare Spending (₹)", min_value=0.0, value=2000.0)

    # Date Input
    start_date = st.date_input("Spending Date (Predict from)", value=datetime.today())
    period_months = st.select_slider("Select Prediction Period (Months)", options=[1, 3, 6, 12, 24, 60], value=12)
    
    if st.button("Calculate Impact"):
        # Fetch Forecast Data
        try:
            res = requests.get(f"{API_BASE}/inflation/forecast")
            if res.status_code != 200:
                st.error("Failed to fetch inflation data")
                return
            forecasts = res.json()
        except:
            st.error("Backend unreachable")
            return
            
        def calculate_future_cost(current_cost, category, months):
            data = forecasts.get(category, [])
            if not data: return current_cost, 0.0
            
            # Since forecasts are fixed from 2020 to 2029 (appx), we need to find relative index?
            # Actually, the 'yhat' is Annual Inflation Rate.
            # We will use the simplified approach:
            # We assume the current_cost provided is valid for 'start_date'.
            # We predict the cost 'months' later.
            
            # Find the rate at the future date
            # We map the future date to the closest available data point index in our fixed forecast
            # Future Date = start_date + months
            future_date = start_date + pd.DateOffset(months=months)
            
            # Since we don't have the full dataframe here to do date matching easily, 
            # we will pick the 'target_idx' simply by adding months to the base.
            # However, for a real feel, let's just use the average rate of the category provided by forecast
            # weighted by the months.
            
            # Better: Let's assume the user wants the projection based on the MODEL's prediction for that future time.
            # We will grab the forecast value for (Today + Months).
            
            # Crude approximation for index: Data starts Jan 2020.
            # Diff in months from Jan 2020 to Future Date.
            start_project = pd.Timestamp("2020-01-01")
            # Ensure future_date is a Timestamp
            future_ts = pd.Timestamp(future_date)
            
            idx = (future_ts.year - start_project.year) * 12 + (future_ts.month - start_project.month)
            
            # Clamp index
            idx = max(0, min(idx, len(data) - 1))
            
            predicted_rate_annual = data[idx]['yhat'] # The rate predicted for that specific future month
            
            # Formula: Future = Current * (1 + rate/100)^(months/12)
            future = current_cost * ((1 + predicted_rate_annual/100) ** (months/12))
            return future, predicted_rate_annual

        f_food, r_food = calculate_future_cost(food_spend, "Food", period_months)
        f_fuel, r_fuel = calculate_future_cost(fuel_spend, "Fuel", period_months)
        f_health, r_health = calculate_future_cost(health_spend, "Healthcare", period_months)
        
        total_now = food_spend + fuel_spend + health_spend + extra_fixed
        total_fut = f_food + f_fuel + f_health + extra_fixed
        extra_cost = total_fut - total_now
        
        savings_now = salary - total_now
        savings_fut = salary - total_fut
        
        # Save to Session for Persistence
        st.session_state.calc_results = {
            "period_months": period_months,
            "r_food": r_food, "f_food": f_food,
            "r_fuel": r_fuel, "f_fuel": f_fuel,
            "r_health": r_health, "f_health": f_health,
            "extra_cost": extra_cost,
            "total_now": total_now,
            "total_fut": total_fut,
            "savings_fut": savings_fut,
            "salary": salary,
            "food_spend": food_spend,
            "fuel_spend": fuel_spend,
            "health_spend": health_spend,
            "extra_fixed": extra_fixed
        }
        
    # --- DISPLAY RESULTS FROM STATE ---
    if 'calc_results' in st.session_state:
        res = st.session_state.calc_results
        
        # Display
        st.divider()
        st.subheader(f"Results for {res['period_months']} Months Forecast")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Food Inflation", f"{res['r_food']:.2f}%", f"₹{int(res['f_food'])}")
        c2.metric("Fuel Inflation", f"{res['r_fuel']:.2f}%", f"₹{int(res['f_fuel'])}")
        c3.metric("Health Inflation", f"{res['r_health']:.2f}%", f"₹{int(res['f_health'])}")
        c4.metric("Extra Cost", f"₹{int(res['extra_cost'])}", delta_color="inverse")
        
        st.write(f"**Total Future Monthly Spending:** ₹{int(res['total_fut'])}")
        
        salary_status = "Unknown"
        if res['savings_fut'] < 0:
            salary_status = "DEFICIT"
            st.error(f"⚠️ DANGER: You will be in debt by ₹{abs(int(res['savings_fut']))}/month!")
        elif res['savings_fut'] < 0.1 * res['salary']:
            salary_status = "AT RISK"
            st.warning(f"⚠️ Warning: Savings will drop to low levels (₹{int(res['savings_fut'])})")
        else:
            salary_status = "SURPLUS"
            st.success(f"✅ Safe: Projected Savings ₹{int(res['savings_fut'])}")
            
        # Visualize
        chart_data = pd.DataFrame({
            "Category": ["Food", "Fuel", "Health", "Fixed"],
            "Now": [res['food_spend'], res['fuel_spend'], res['health_spend'], res['extra_fixed']],
            "Future": [res['f_food'], res['f_fuel'], res['f_health'], res['extra_fixed']]
        })
        df_melt = chart_data.melt("Category", var_name="Time", value_name="Cost")
        fig = px.bar(df_melt, x="Category", y="Cost", color="Time", barmode="group",
                     color_discrete_sequence=["#00CC96", "#EF553B"])
        st.plotly_chart(fig, use_container_width=True)
        
        # Determine Most Affected
        item_increases = {
            "Food": res['f_food'] - res['food_spend'],
            "Fuel": res['f_fuel'] - res['fuel_spend'],
            "Healthcare": res['f_health'] - res['health_spend']
        }
        most_affected = max(item_increases, key=item_increases.get) if max(item_increases.values()) > 0 else "None"
        
        # Save Button (Now outside the main button logic)
        if st.button("Save & Return to Dashboard"):
            payload = {
                "user_id": st.session_state.user_id,
                "salary": res['salary'],
                "food": res['food_spend'],
                "fuel": res['fuel_spend'],
                "health": res['health_spend'],
                "extra_spend": res['extra_fixed'],
                "total_spend": res['total_now'],
                "future_total_spend": res['total_fut'],
                "salary_status": salary_status,
                "most_affected_category": most_affected
            }
            success = False
            try:
                s_res = requests.post(f"{API_BASE}/data/spending", json=payload)
                if s_res.status_code == 201:
                    success = True
                else:
                    st.error("Failed to save.")
            except Exception as e:
                st.error(f"Connection failed: {e}")
            
            if success:
                 st.success("Data Saved to Profile!")
                 st.session_state.current_page = "User Dashboard"
                 st.rerun()
