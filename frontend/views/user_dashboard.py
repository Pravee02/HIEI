import streamlit as st
import pandas as pd
import requests

from utils.api import API_URL

API_BASE = f"{API_URL}/api"

def display_user_dashboard():
    # --- Custom CSS for FinTech Look ---
    st.markdown("""
        <style>
        .dashboard-hero {
            background: linear-gradient(135deg, #0E1117 0%, #161B22 100%);
            padding: 30px;
            border-radius: 12px;
            border: 1px solid #30363D;
            margin-bottom: 25px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        .hero-title {
            font-size: 2.2rem;
            font-weight: 700;
            color: #FFFFFF;
            margin-bottom: 10px;
        }
        .hero-subtitle {
            font-size: 1.1rem;
            color: #8B949E;
            margin-bottom: 5px;
        }
        .hero-status {
            font-size: 0.85rem;
            color: #00CC96; /* Tech Green */
            font-family: 'Courier New', monospace;
            opacity: 0.8;
        }
        
        /* Insight Cards */
        .metric-card {
            background-color: #161B22; 
            border: 1px solid #30363D;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }
        .metric-label { font-size: 0.9rem; color: #8B949E; margin-bottom: 5px; }
        .metric-value { font-size: 1.5rem; font-weight: 600; color: #FAFAFA; }
        .metric-sub { font-size: 0.8rem; color: #58A6FF; margin-top: 5px; }

        /* Action Tiles */
        .action-tile {
            background-color: #21262D;
            border: 1px solid #30363D;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            transition: transform 0.2s, border-color 0.2s;
            cursor: pointer;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: 10px;
        }
        .action-tile:hover {
            transform: translateY(-2px);
            border-color: #58A6FF;
        }
        .action-icon { font-size: 2rem; margin-bottom: 10px; }
        .action-text { color: #C9D1D9; font-weight: 500; text-decoration: none; }

        /* Educational Strip */
        .edu-strip {
            background-color: #1F2428; /* Slightly lighter/different tone */
            border-left: 4px solid #A371F7; /* Purple accent */
            padding: 15px 20px;
            border-radius: 4px;
            margin-top: 30px;
            font-style: italic;
            color: #C9D1D9;
        }
        </style>
    """, unsafe_allow_html=True)

    # 1️⃣ Hero Section
    username = st.session_state.get('username', 'User')
    
    st.markdown(f"""
        <div class="dashboard-hero">
            <div class="hero-title">Welcome back, {username}</div>
            <div class="hero-subtitle">Monitor inflation impact, spending behavior, and financial readiness in one place.</div>
            <div class="hero-status">Logged-in User | System Status: Active ●</div>
        </div>
    """, unsafe_allow_html=True)

    # 2️⃣ Key Insight Cards
    # Gather Data (Safe Get)
    last_salary = st.session_state.get('last_salary', 0)
    last_savings = st.session_state.get('last_savings', 0)
    
    # Check History for Simulation Status
    sim_status = "No Data"
    history_count = 0
    history_data = [] # Store for later use
    
    try:
        user_id = st.session_state.user_id
        res = requests.get(f"{API_BASE}/data/history/{user_id}")
        if res.status_code == 200:
            history_data = res.json()
            history_count = len(history_data)
            if history_count > 0:
                sim_status = "Active"
    except:
        pass

    # Determine Readiness
    readiness = "Neutral 😐"
    readiness_color = "#8B949E" # Grey
    
    if last_salary > 0:
        savings_rate = last_savings / last_salary
        if savings_rate < 0:
            readiness = "Alert ⚠️"
            readiness_color = "#EF553B" # Red
        elif savings_rate > 0.2:
            readiness = "Stable 🛡️"
            readiness_color = "#00CC96" # Green
    elif history_count > 0:
         readiness = "Review Needed 📝"

    # Display Metrics Row
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Last Recorded Salary</div>
                <div class="metric-value">{'₹' + str(last_salary) if last_salary > 0 else 'No data yet'}</div>
                <div class="metric-sub">Monthly Income</div>
            </div>
        """, unsafe_allow_html=True)
    
    with c2:
        # Spending is roughly Salary - Savings
        estimated_spending = last_salary - last_savings if last_salary > 0 else 0
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Est. Monthly Spending</div>
                <div class="metric-value">{'₹' + str(estimated_spending) if last_salary > 0 else 'No data yet'}</div>
                <div class="metric-sub">Based on Simulation</div>
            </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Simulation Status</div>
                <div class="metric-value">{sim_status}</div>
                <div class="metric-sub">{history_count} Runs recorded</div>
            </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
            <div class="metric-card" style="border-bottom: 3px solid {readiness_color};">
                <div class="metric-label">Financial Readiness</div>
                <div class="metric-value" style="font-size: 1.2rem; color:{readiness_color}">{readiness}</div>
                <div class="metric-sub">Indicator</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 3️⃣ Inflation Simulation Activity Panel
    col_activity, col_actions = st.columns([2, 1])
    
    with col_activity:
        st.subheader(" Recent Inflation Simulations")
        
        if history_count > 0:
            # Show strictly relevant columns to keep it clean
            df = pd.DataFrame(history_data)
            # Rename for display if columns exist
            display_cols = ['timestamp', 'monthly_income', 'total_expenses', 'inflation_rate']
            final_cols = [c for c in display_cols if c in df.columns]
            
            if final_cols:
                st.dataframe(
                    df[final_cols].style.format({"monthly_income": "₹{:.0f}", "total_expenses": "₹{:.0f}", "inflation_rate": "{:.1f}%"}),
                    use_container_width=True,
                    height=250,
                    hide_index=True
                )
            else:
                st.dataframe(df, use_container_width=True, height=250)
        else:
            # Empty State
            st.info("You haven't run any inflation simulations yet.")
            st.markdown("""
                <div style="background-color: #161B22; padding: 20px; border-radius: 8px; text-align: center; border: 1px dashed #30363D;">
                    <p style="color: #8B949E;">Start by calculating how inflation affects your household budget.</p>
                </div>
            """, unsafe_allow_html=True)

    # 4️⃣ Action Shortcuts Section
    with col_actions:
        st.subheader("⚡ Quick Actions")
        
        # Note: In Streamlit, buttons rerun the script. We'll use them to maybe set a hint or just be visual.
        # Since we can't easily change the Sidebar Radio state from here without complex callback logic
        # that might conflict with st.sidebar, we will make these "Navigational cues".
        
        g1, g2 = st.columns(2)
        with g1:
            st.markdown("""
            <div class="action-tile">
                <div class="action-icon">➕</div>
                <div class="action-text">Inflation<br>Calculator</div>
            </div>
            """, unsafe_allow_html=True)
        with g2:
             st.markdown("""
            <div class="action-tile">
                <div class="action-icon">🏢</div>
                <div class="action-text">Company<br>Analysis</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("") # Spacer

        g3, g4 = st.columns(2)
        with g3:
             st.markdown("""
            <div class="action-tile">
                <div class="action-icon">📉</div>
                <div class="action-text">Inflation<br>Dashboard</div>
            </div>
            """, unsafe_allow_html=True)
        with g4:
             st.markdown("""
            <div class="action-tile">
                <div class="action-icon">🛡️</div>
                <div class="action-text">Insurance<br>Check</div>
            </div>
            """, unsafe_allow_html=True)

        st.caption("Select from the sidebar menu to access these tools.")

    # 5️⃣ Educational Insight Strip
    st.markdown("""
        <div class="edu-strip">
            💡 "Understanding inflation helps households plan spending, savings, and investment decisions more effectively."
        </div>
    """, unsafe_allow_html=True)


def display_policy_makers_list():
    st.header("Contact Policy Makers")
    st.markdown("Below is the list of registered Policy Makers you can reach out to.")
    
    try:
        res = requests.get(f"{API_BASE}/data/policy-makers")
        if res.status_code == 200:
            pms = res.json()
            if pms:
                for pm in pms:
                    with st.expander(f"🏛️ {pm['username']} - {pm['policy_area']}"):
                        st.write(f"**Policy Area:** {pm['policy_area']}")
                        st.write(f"**Phone:** {pm['phone']}")
                        st.write(f"**Action:** [Call Now](tel:{pm['phone']})")
            else:
                st.info("No Policy Makers registered yet.")
        else:
            st.error("Failed to fetch list.")
    except Exception as e:
        st.error(f"Connection Error: {e}")
