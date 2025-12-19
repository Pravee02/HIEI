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
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .metric-label { font-size: 0.9rem; color: #8B949E; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px;}
        .metric-value { font-size: 1.6rem; font-weight: 700; color: #FAFAFA; margin-bottom: 5px; }
        .metric-sub { font-size: 0.85rem; color: #7D8590; line-height: 1.4; }
        .metric-highlight { color: #58A6FF; font-weight: 500; }

        /* Empty State Panel */
        .empty-state-panel {
            background-color: #161B22;
            border: 1px dashed #30363D;
            border-radius: 8px;
            padding: 40px;
            text-align: center;
            color: #8B949E;
        }
        .empty-state-title { font-size: 1.2rem; color: #FAFAFA; margin-bottom: 10px; font-weight: 600; }
        .empty-state-text { font-size: 0.95rem; margin-bottom: 0; }

        /* Action Tiles */
        .action-tile {
            background-color: #21262D;
            border: 1px solid #30363D;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            transition: all 0.2s ease;
            cursor: pointer;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: 8px;
        }
        .action-tile:hover {
            transform: translateY(-2px);
            border-color: #58A6FF;
            background-color: #292E36;
        }
        .action-icon { font-size: 1.8rem; margin-bottom: 5px; }
        .action-title { color: #FAFAFA; font-weight: 600; font-size: 1rem; }
        .action-desc { color: #8B949E; font-size: 0.8rem; }

        /* Educational Strip */
        .edu-strip {
            background-color: #161B22; 
            border-left: 4px solid #A371F7; /* Purple accent */
            padding: 20px;
            border-radius: 4px;
            margin-top: 30px;
            color: #C9D1D9;
            display: flex;
            align-items: start;
            gap: 15px;
        }
        .edu-icon { font-size: 1.5rem; }
        .edu-text { font-style: italic; font-size: 0.95rem; line-height: 1.5; }
        </style>
    """, unsafe_allow_html=True)

    # 1️⃣ Hero Section
    username = st.session_state.get('username', 'User')
    
    st.markdown(f"""
        <div class="dashboard-hero">
            <div class="hero-title">Hello, {username} 👋</div>
            <div class="hero-subtitle">Here is your financial overview and inflation impact analysis.</div>
            <div class="hero-status">System Status: Active ●</div>
        </div>
    """, unsafe_allow_html=True)

    # 2️⃣ Key Insight Cards
    # Gather Data (Safe Get)
    last_salary = st.session_state.get('last_salary', 0)
    last_savings = st.session_state.get('last_savings', 0)
    
    # Check History for Simulation Status
    sim_status = "No runs yet"
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
    readiness_desc = "Not enough data to analyze."
    readiness_color = "#8B949E" # Grey
    
    if last_salary > 0:
        savings_rate = last_savings / last_salary
        if savings_rate < 0:
            readiness = "Alert ⚠️"
            readiness_desc = "Spending exceeds income."
            readiness_color = "#EF553B" # Red
        elif savings_rate > 0.2:
            readiness = "Stable 🛡️"
            readiness_desc = "Healthy savings buffer."
            readiness_color = "#00CC96" # Green
        else:
             readiness = "Caution ⚠️"
             readiness_desc = "Savings are low."
             readiness_color = "#E1AD01" # Orange
    elif history_count > 0:
         readiness = "Review Needed 📝"
         readiness_desc = "Update your inputs."

    # Display Metrics Row
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Monthly Income</div>
                <div class="metric-value">{'₹' + str(int(last_salary)) if last_salary > 0 else '—'}</div>
                <div class="metric-sub">Based on your last input</div>
            </div>
        """, unsafe_allow_html=True)
    
    with c2:
        # Spending is roughly Salary - Savings
        estimated_spending = last_salary - last_savings if last_salary > 0 else 0
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Est. Monthly Spend</div>
                <div class="metric-value">{'₹' + str(int(estimated_spending)) if last_salary > 0 else '—'}</div>
                <div class="metric-sub">Projected household expense</div>
            </div>
        """, unsafe_allow_html=True)


    with c3:
        # Improved Simulation Status
        if history_count > 0:
            val_text = f"{history_count}"
            sub_text = "Total simulations run"
            val_style = ""
        else:
            val_text = "No simulations"
            sub_text = "Run calculator to start"
            val_style = "font-size: 1.2rem; color: #8B949E;"
            
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Analysis History</div>
                <div class="metric-value" style="{val_style}">{val_text}</div>
                <div class="metric-sub">{sub_text}</div>
            </div>
        """, unsafe_allow_html=True)


    with c4:
        st.markdown(f"""
            <div class="metric-card" style="border-bottom: 3px solid {readiness_color};">
                <div class="metric-label">Financial Readiness</div>
                <div class="metric-value" style="font-size: 1.4rem; color:{readiness_color}">{readiness}</div>
                <div class="metric-sub">{readiness_desc}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 3️⃣ Inflation Simulation Activity Panel
    st.subheader("📊 Recent Activity")
    col_activity, col_actions = st.columns([2, 1])
    
    with col_activity:
        if history_count > 0:
            t1, t2 = st.columns([3, 1])
            t1.caption("Showing your latest inflation impact calculations.")
            
            # Show strictly relevant columns to keep it clean
            df = pd.DataFrame(history_data)
            # Rename for display if columns exist
            display_cols = ['timestamp', 'monthly_income', 'total_expenses', 'inflation_rate']
            final_cols = [c for c in display_cols if c in df.columns]
            
            if final_cols:
                # Rename columns for friendly display
                df_show = df[final_cols].rename(columns={
                    'timestamp': 'Date',
                    'monthly_income': 'Income', 
                    'total_expenses': 'Expenses', 
                    'inflation_rate': 'Inf. Rate'
                })
                st.dataframe(
                    df_show.style.format({"Income": "₹{:.0f}", "Expenses": "₹{:.0f}", "Inf. Rate": "{:.1f}%"}),
                    use_container_width=True,
                    height=250,
                    hide_index=True
                )
            else:
                st.dataframe(df, use_container_width=True, height=250)
        else:
            # Enhanced Empty State
            st.markdown("""
                <div class="empty-state-panel">
                    <div class="empty-state-title">You haven’t analyzed inflation yet</div>
                    <p class="empty-state-text">Start with the Inflation Calculator to see how future price rises will affect your specific household budget.</p>
                </div>
            """, unsafe_allow_html=True)

    # 4️⃣ Action Shortcuts Section
    with col_actions:
        # Note: In Streamlit, buttons rerun the script. Visual cues only.
        
        g1, g2 = st.columns(2)
        with g1:
            st.markdown("""
            <div class="action-tile">
                <div class="action-icon">➕</div>
                <div class="action-title">Calculator</div>
                <div class="action-desc">Analyze future impact</div>
            </div>
            """, unsafe_allow_html=True)
        with g2:
             st.markdown("""
            <div class="action-tile">
                <div class="action-icon">🏢</div>
                <div class="action-title">Analysis</div>
                <div class="action-desc">Check companies</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("") # Spacer

        g3, g4 = st.columns(2)
        with g3:
             st.markdown("""
            <div class="action-tile">
                <div class="action-icon">📉</div>
                <div class="action-title">Dashboard</div>
                <div class="action-desc">Forecast trends</div>
            </div>
            """, unsafe_allow_html=True)
        with g4:
             st.markdown("""
            <div class="action-tile">
                <div class="action-icon">🛡️</div>
                <div class="action-title">Insurance</div>
                <div class="action-desc">Review coverage</div>
            </div>
            """, unsafe_allow_html=True)

        st.caption("Select from the sidebar to access.")

    # 5️⃣ Educational Insight Strip
    st.markdown("""
        <div class="edu-strip">
            <div class="edu-icon">💡</div>
            <div class="edu-text">
                "Understanding inflation helps households plan spending, savings, and investment decisions more effectively. 
                Regularly checking your readiness score can prevent future financial stress."
            </div>
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
