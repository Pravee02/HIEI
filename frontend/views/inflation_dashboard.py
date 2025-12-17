import streamlit as st
import pandas as pd
import plotly.express as px
import requests

API_BASE = "http://127.0.0.1:5000/api"

def display_inflation_dashboard():
    st.header("Global Inflation Forecast (5 Years)")
    st.markdown("Prophet-based machine learning forecast for key commodities.")
    
    try:
        res = requests.get(f"{API_BASE}/inflation/forecast")
        if res.status_code == 200:
            forecasts = res.json()
            
            # Combine into one DF for plotting
            all_data = []
            for cat, points in forecasts.items():
                for p in points:
                    all_data.append({
                        "Date": p['ds'],
                        "Inflation Rate (%)": p['yhat'],
                        "Category": cat
                    })
            
            df = pd.DataFrame(all_data)
            df['Date'] = pd.to_datetime(df['Date'])
            
            fig = px.line(df, x="Date", y="Inflation Rate (%)", color="Category", 
                          title="Predicted Inflation Trends (2024-2029)",
                          color_discrete_sequence=["#00CC96", "#EF553B", "#636EFA"])
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **Analysis:**
            - **Food:** Projected seasonal spikes with underlying trend.
            - **Fuel:** High volatility expected.
            - **Healthcare:** Steady compounding increase.
            """)
        else:
            st.error("Failed to load forecast data.")
    except Exception as e:
        st.error(f"Connection Error: {e}")
