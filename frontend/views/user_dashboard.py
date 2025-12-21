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

    # NEW: Fallback or Sync logic to ensure we have data for display
    # If session is empty but we have history, use the latest history item
    # We also need these variables even if not 0, so let's check latest history always if available?
    # Actually, let's prioritize history for the dashboard display to be accurate to "Last Analysis"
    
    last_salary = 0
    total_spend = 0
    most_affected = "—"
    
    if history_count > 0:
        latest = history_data[0]
        last_salary = latest.get('salary', 0)
        total_spend = latest.get('total_spend', 0)
        most_affected = latest.get('most_affected', '—')
        if most_affected == "Stable": most_affected = "None"
        
        # Sync session state just in case calculator needs it (though calculator overwrites usually)
        st.session_state['last_salary'] = last_salary
        if total_spend > 0:
             st.session_state['last_savings'] = last_salary - total_spend

    # Fallback: If no history (or salary 0), check if user just ran the calculator in this session
    if last_salary == 0 and 'calc_results' in st.session_state:
        res = st.session_state.calc_results
        last_salary = res.get('salary', 0)
        if total_spend == 0:
            total_spend = res.get('total_now', 0)
        # Note: We don't have 'most_affected' easily available in simple calc_results unless we re-derive it, 
        # but the prompt specifically asked for Income/Spend. 
        # Actually calculator does calculate 'most_affected' but doesn't pass it in 'calc_results' explicitly as a simple string always?
        # Let's check calculator.py... it saves 'r_food' etc. 
        # Ideally we stick to the main request: Fix Monthly Income.


    # Display Metrics Row (3 Cards as requested)
    c1, c2, c3 = st.columns(3)
    
    # CARD 1: Monthly Income
    with c1:
        if last_salary > 0:
            val_text = f"₹{int(last_salary):,}"
            sub_text = "Based on your last input in the Inflation Calculator"
            val_color = "#FAFAFA"
        else:
            val_text = "—"
            sub_text = "Based on your last input in the Inflation Calculator"
            val_color = "#8B949E"

        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Monthly Income</div>
                <div class="metric-value" style="color: {val_color}; font-size: 1.6rem;">{val_text}</div>
                <div class="metric-sub">{sub_text}</div>
            </div>
        """, unsafe_allow_html=True)
    
    # CARD 2: Monthly Total Spending
    with c2:
        if total_spend > 0:
            val_text = f"₹{int(total_spend):,}"
            sub_text = "Combined household expenses per month"
            val_color = "#FAFAFA"
        else:
            val_text = "—"
            sub_text = "Combined household expenses per month"
            val_color = "#8B949E"

        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Monthly Total Spending</div>
                <div class="metric-value" style="color: {val_color}; font-size: 1.6rem;">{val_text}</div>
                <div class="metric-sub">{sub_text}</div>
            </div>
        """, unsafe_allow_html=True)


    # CARD 3: Most Affected Expense
    with c3:
        if most_affected and most_affected != "—" and most_affected != "None":
            val_text = most_affected
            sub_text = "Based on latest inflation analysis"
            val_color = "#EF553B" # Highlight color for impact
        else:
            val_text = "—"
            sub_text = "Based on latest inflation analysis"
            val_color = "#8B949E"
            
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Most Affected Expense</div>
                <div class="metric-value" style="color: {val_color}; font-size: 1.6rem;">{val_text}</div>
                <div class="metric-sub">{sub_text}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")

    # 3️⃣ High Tech Command Center (Replaces Empty Activity)
    
    # If we have history, show it. If not, don't show "Empty", just show Controls.
    if history_count > 0:
         st.subheader("📊 Inflation Analytics Log")
         
         # Show clean dataframe
         df = pd.DataFrame(history_data)
         # Map backend keys to display columns
         # Keys from data_routes: date, salary, total_spend, future_total_spend, salary_status, most_affected
         
         # Just rename them directly
         if not df.empty:
            df_show = df.rename(columns={
                'date': 'Date',
                'salary': 'Income',
                'total_spend': 'Expenses',
                'future_total_spend': 'Projected',
                'salary_status': 'Status',
                'most_affected': 'Impact'
            })
            
            # Select relevant columns
            cols_to_show = ['Date', 'Income', 'Expenses', 'Projected', 'Status']
            # Filter if they exist
            final_show = df_show[[c for c in cols_to_show if c in df_show.columns]]

            st.dataframe(
                final_show.style.format({"Income": "₹{:.0f}", "Expenses": "₹{:.0f}", "Projected": "₹{:.0f}"}, na_rep="-"),
                use_container_width=True,
                height=250,
                hide_index=True
            )
         else:
            st.info("No data available.")
         
         st.markdown("---")

    # 4️⃣ Command Center Actions (Functional)
    st.subheader("🚀 Quick Actions")
    
    # Custom CSS for buttons to make them look larger/techy
    st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #21262D;
        color: #58A6FF;
        border: 1px solid #30363D;
        height: 80px;
        width: 100%;
        font-size: 18px;
        border-radius: 8px;
        transition: all 0.2s;
    }
    div.stButton > button:first-child:hover {
        background-color: #292E36;
        border-color: #58A6FF;
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

    ac1, ac2, ac3, ac4 = st.columns(4)
    
    with ac1:
        if st.button("➕ Calculator", use_container_width=True):
            st.session_state.current_page = "Inflation Calculator"
            st.rerun()
            
    with ac2:
        if st.button("🏢 Analysis", use_container_width=True):
            st.session_state.current_page = "Company Analysis"
            st.rerun()
            
    with ac3:
        if st.button("📉 Dashboard", use_container_width=True):
            st.session_state.current_page = "Inflation Dashboard"
            st.rerun()
            
    with ac4:
        if st.button("🛡️ Insurance", use_container_width=True):
            st.session_state.current_page = "Insurance Information"
            st.rerun()

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
