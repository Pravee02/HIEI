import streamlit as st
import pandas as pd
import plotly.express as px
import requests

from utils.api import API_URL

API_BASE = f"{API_URL}/api"

def display_inflation_dashboard():
    # --- Professional Header ---
    st.markdown("""
        <div style="padding-bottom: 20px; border-bottom: 1px solid #30363D; margin-bottom: 20px;">
            <h2 style="margin: 0; color: #FAFAFA; font-size: 2rem;">Global Inflation Forecast</h2>
            <p style="margin: 5px 0 0; color: #8B949E; font-size: 1rem;">
                Machine learning projections for key household commodities.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    try:
        res = requests.get(f"{API_BASE}/inflation/forecast")
        if res.status_code == 200:
            forecasts = res.json()
            
            # Combine into one DF
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
            
            # --- 1. Interactive Controls ---
            c_ctrl1, c_ctrl2 = st.columns([3, 1])
            
            with c_ctrl1:
                # Category Toggle
                available_cats = sorted(df['Category'].unique().tolist())
                selected_cats = st.multiselect("Filter Categories", available_cats, default=available_cats)
                
            with c_ctrl2:
                # Time Range Selector
                time_range = st.selectbox("View Horizon", ["12 Months", "2 Years", "5 Years (All)"], index=2)
            
            # --- Logic: Filter Data ---
            if not selected_cats:
                st.warning("Please select at least one category to view trends.")
            else:
                df_filtered = df[df['Category'].isin(selected_cats)]
                
                # Filter by Time Range (assuming forecast starts from min date)
                start_date = df['Date'].min()
                if time_range == "12 Months":
                    end_date = start_date + pd.DateOffset(months=12)
                    df_filtered = df_filtered[df_filtered['Date'] <= end_date]
                elif time_range == "2 Years":
                    end_date = start_date + pd.DateOffset(months=24)
                    df_filtered = df_filtered[df_filtered['Date'] <= end_date]
                
                # --- 2. Interactive Chart ---
                fig = px.line(df_filtered, x="Date", y="Inflation Rate (%)", color="Category",
                              color_discrete_map={"Food": "#00CC96", "Fuel": "#EF553B", "Healthcare": "#636EFA"},
                              template="plotly_dark")
                
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=10, r=10, t=10, b=10),
                    height=450,
                    hovermode="x unified",
                    font=dict(family="Inter, sans-serif", size=12, color="#C9D1D9"),
                    xaxis=dict(showgrid=False, showline=True, linecolor="#30363D"),
                    yaxis=dict(showgrid=True, gridcolor="#21262D", zeroline=False),
                    legend=dict(orientation="h", y=1.05, x=0, bgcolor="rgba(0,0,0,0)")
                )
                
                # Custom Hover
                fig.update_traces(hovertemplate="%{y:.2f}%<extra></extra>")
                
                st.plotly_chart(fig, use_container_width=True)
            
            # --- 3. Professional Insight Cards ---
            st.markdown("### ⚡ Market Insights")
            
            ic1, ic2, ic3 = st.columns(3)
            
            def insight_card(title, trend_label, desc, color):
                return f"""
                <div style="background-color: #161B22; border: 1px solid #30363D; border-left: 4px solid {color}; padding: 16px; border-radius: 6px; height: 100%;">
                    <div style="color: #8B949E; font-size: 0.8rem; text-transform: uppercase; font-weight: 600; margin-bottom: 4px;">{title}</div>
                    <div style="color: #FAFAFA; font-size: 1rem; font-weight: 700; margin-bottom: 6px;">{trend_label}</div>
                    <div style="color: #6E7681; font-size: 0.85rem; line-height: 1.4;">{desc}</div>
                </div>
                """
            
            with ic1:
                st.markdown(insight_card("Food", "Seasonal Trends 📈", "Seasonal fluctuations with upward trend", "#00CC96"), unsafe_allow_html=True)
            with ic2:
                st.markdown(insight_card("Fuel", "High Volatility ⚡", "High volatility over forecast period", "#EF553B"), unsafe_allow_html=True)
            with ic3:
                st.markdown(insight_card("Healthcare", "Steady Compounding 🛡️", "Consistent long-term increase", "#636EFA"), unsafe_allow_html=True)

        else:
            st.error("Unable to load forecast data from server.")
    except Exception as e:
        st.error(f"Connection Error: {e}")

