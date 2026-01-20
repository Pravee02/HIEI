import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime

from utils.api import API_URL

API_BASE = f"{API_URL}/api"

def display_calculator():
    # Load CSS
    import os
    css_path = os.path.join(os.path.dirname(__file__), '../assets/style.css')
    try:
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except:
        pass

    # --- HERO SECTION ---
    st.markdown("""
        <div style="margin-bottom: 2rem;">
            <h1 style="margin-bottom: 0.5rem; background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Inflation Calculator & Planner</h1>
            <p style="color: #94a3b8; font-size: 1.1rem;">Smulate future inflation impact on your personal household budget and plan ahead.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # --- INPUT SECTION (CARDS) ---
    c_left, c_right = st.columns(2)
    
    with c_left:
        st.markdown('<div class="calc-card"><h4>💰 Income & Fixed Expenses</h4>', unsafe_allow_html=True)
        salary = st.number_input("Monthly Salary (₹)", min_value=0.0, value=50000.0, step=1000.0)
        extra_fixed = st.number_input("EMI / Other Fixed Spending (₹)", min_value=0.0, value=15000.0, step=500.0)
        group = st.selectbox("Household Group", ["Urban Poor", "Urban Rich", "Rural Poor", "Rural Rich"])
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c_right:
        st.markdown('<div class="calc-card"><h4>🛒 Variable Expenses (Monthly)</h4>', unsafe_allow_html=True)
        food_spend = st.number_input("Food Spending (₹)", min_value=0.0, value=8000.0, step=500.0)
        fuel_spend = st.number_input("Fuel/Transport Spending (₹)", min_value=0.0, value=3000.0, step=500.0)
        health_spend = st.number_input("Healthcare Spending (₹)", min_value=0.0, value=2000.0, step=500.0)
        st.markdown('</div>', unsafe_allow_html=True)

    # Date Input & Action
    st.markdown('<div class="section-header-calc">📅 Prediction Parameters</div>', unsafe_allow_html=True)
    
    # Clean slider layout
    start_date = st.date_input("Spending Date (Predict from)", value=datetime.today())
    period_months = st.select_slider("Select Prediction Period (Months)", options=[1, 3, 6, 12, 24, 60], value=12)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Calculate Impact", type="primary", use_container_width=True):
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
        
        # Display Dashboard
        st.markdown(f'<div class="section-header-calc">📊 Forecast Results ({res["period_months"]} Months)</div>', unsafe_allow_html=True)
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Food Inflation", f"{res['r_food']:.1f}%", f"+ ₹{int(res['f_food'] - res['food_spend'])}")
        c2.metric("Fuel Inflation", f"{res['r_fuel']:.1f}%", f"+ ₹{int(res['f_fuel'] - res['fuel_spend'])}")
        c3.metric("Health Inflation", f"{res['r_health']:.1f}%", f"+ ₹{int(res['f_health'] - res['health_spend'])}")
        c4.metric("Extra Monthly cost", f"₹{int(res['extra_cost'])}", delta_color="inverse")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Savings Status Banner
        salary_status = "Unknown"
        if res['savings_fut'] < 0:
            salary_status = "DEFICIT"
            banner_class = "danger"
            banner_icon = "🚨"
            banner_msg = f"CRITICAL: You will be in DEBT by ₹{abs(int(res['savings_fut']))}/month!"
        elif res['savings_fut'] < 0.1 * res['salary']:
            salary_status = "AT RISK"
            banner_class = "risk"
            banner_icon = "⚠️"
            banner_msg = f"WARNING: Savings dropping to critical levels (₹{int(res['savings_fut'])})"
        else:
            salary_status = "SURPLUS"
            banner_class = "safe"
            banner_icon = "✅"
            banner_msg = f"SAFE: Projected Savings ₹{int(res['savings_fut'])}"
            
        st.markdown(f"""
            <div class="savings-banner {banner_class}">
                <div style="font-size: 1.5rem;">{banner_icon}</div>
                <div>{banner_msg}</div>
            </div>
        """, unsafe_allow_html=True)
            
        # Visualize
        c_chart, c_details = st.columns([2, 1])
        
        with c_chart:
            st.markdown("##### Spending Comparison")
            chart_data = pd.DataFrame({
                "Category": ["Food", "Fuel", "Health", "Fixed"],
                "Now": [res['food_spend'], res['fuel_spend'], res['health_spend'], res['extra_fixed']],
                "Future": [res['f_food'], res['f_fuel'], res['f_health'], res['extra_fixed']]
            })
            df_melt = chart_data.melt("Category", var_name="Time", value_name="Cost")
            fig = px.bar(df_melt, x="Category", y="Cost", color="Time", barmode="group",
                         color_discrete_sequence=["#2dd4bf", "#f43f5e"]) # Teal vs Red
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#cbd5e1")
            st.plotly_chart(fig, use_container_width=True)
        
        with c_details:
             st.markdown("##### Quick Summary")
             st.markdown(f"""
                <div style="background: #1e293b; padding: 1rem; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);">
                    <div style="display:flex; justify-content:space-between; margin-bottom: 0.5rem;">
                        <span style="color:#94a3b8">Current Total:</span>
                        <span style="font-weight:600">₹{int(res['total_now'])}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-bottom: 0.5rem;">
                        <span style="color:#94a3b8">Future Total:</span>
                        <span style="font-weight:600; color:#f43f5e">₹{int(res['total_fut'])}</span>
                    </div>
                    <hr style="border-color: rgba(255,255,255,0.1); margin: 0.5rem 0;">
                    <div style="display:flex; justify-content:space-between;">
                        <span style="color:#94a3b8">Net Impact:</span>
                        <span style="font-weight:600; color:#f43f5e">+ ₹{int(res['extra_cost'])}</span>
                    </div>
                </div>
             """, unsafe_allow_html=True)
             
             st.markdown("<br>", unsafe_allow_html=True)
             
             # Determine Most Affected
             item_increases = {
                "Food": res['f_food'] - res['food_spend'],
                "Fuel": res['f_fuel'] - res['fuel_spend'],
                "Healthcare": res['f_health'] - res['health_spend']
             }
             most_affected = max(item_increases, key=item_increases.get) if max(item_increases.values()) > 0 else "None"
             
             if st.button("Save Logic to Profile", use_container_width=True):
                 if 'user_id' not in st.session_state:
                     st.error("Please login to save.")
                 else:
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
                    try:
                        s_res = requests.post(f"{API_BASE}/data/spending", json=payload)
                        if s_res.status_code == 201:
                            st.success("Data Saved!")
                            st.session_state.current_page = "User Dashboard"
                            st.rerun()
                        else:
                            st.error("Failed to save.")
                    except Exception as e:
                        st.error(f"Connection error: {e}")
