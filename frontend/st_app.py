import streamlit as st
from views.auth import user_login, user_register, policy_login, policy_register
from views.user_dashboard import display_user_dashboard
from views.policy_dashboard import display_policy_dashboard
from views.inflation_dashboard import display_inflation_dashboard
from views.investment import display_investment_page, display_insurance_page
from views.company_analysis import display_company_analysis
# from views.user_list import ...

# Helper to clear session
def logout():
    for key in ['user_token', 'pm_token', 'user_id', 'pm_id', 'username']:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

st.set_page_config(page_title="HIEI System", page_icon="💠", layout="wide")

# Styling
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    div[data-testid="stSidebar"] { background-color: #161B22; }
    </style>
    """, unsafe_allow_html=True)

def main():
    if 'user_token' not in st.session_state: st.session_state.user_token = None
    if 'pm_token' not in st.session_state: st.session_state.pm_token = None
    
    st.sidebar.title("💠 HIEI System")
    
    # --- Navigation Logic ---
    
    if st.session_state.user_token:
        # USER MODE
        st.sidebar.success(f"User: {st.session_state.get('username')}")
        if "current_page" not in st.session_state:
            st.session_state.current_page = "User Dashboard"

        nav_options = [
            "User Dashboard",
            "Inflation Calculator",
            "Inflation Dashboard",
            "Investments",
            "Company Analysis",
            "Insurance Information",
            "Logout"
        ]
        
        try:
            nav_index = nav_options.index(st.session_state.current_page)
        except:
            nav_index = 0

        # Sync state with sidebar
        menu = st.sidebar.radio("Menu", nav_options, index=nav_index)
        
        if menu != st.session_state.current_page:
            st.session_state.current_page = menu
            st.rerun()
        
        if menu == "User Dashboard":
            display_user_dashboard()
        elif menu == "Inflation Calculator":
            # We can put calculator inside user dashboard or separate
            from views.calculator import display_calculator
            display_calculator()
        elif menu == "Inflation Dashboard":
            display_inflation_dashboard()
        elif menu == "Investments":
            display_investment_page()
        elif menu == "Company Analysis":
            display_company_analysis()
        elif menu == "Insurance Information":
            display_insurance_page()
        elif menu == "Logout":
            logout()
            
    elif st.session_state.pm_token:
        # POLICY MAKER MODE
        st.sidebar.warning(f"Policy Maker: {st.session_state.get('username')}")
        
        # State-based Nav
        if "pm_page" not in st.session_state:
            st.session_state.pm_page = "Policy Dashboard"
            
        pm_nav_options = [
            "Policy Dashboard",
            "Policy Insights",
            "Contact Users",
            "Logout"
        ]
        
        try:
            curr_index = pm_nav_options.index(st.session_state.pm_page)
        except ValueError:
            curr_index = 0
            
        menu = st.sidebar.radio("Menu", pm_nav_options, index=curr_index)
        
        if menu != st.session_state.pm_page:
            st.session_state.pm_page = menu
            st.rerun()
        
        if menu == "Policy Dashboard":
            # Load CSS
            try:
                import os
                css_path = os.path.join(os.path.dirname(__file__), 'assets/style.css')
                with open(css_path) as f:
                    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
            except:
                pass

            # HERO SECTION
            st.markdown("""
                <div class="policy-hero">
                    <div class="policy-title">Policy Maker Dashboard</div>
                    <div class="policy-subtitle">Centralized policy monitoring and economic impact control</div>
                </div>
            """, unsafe_allow_html=True)
            
            # INSIGHTS GRID
            st.markdown("### 📊 Live System Status")
            st.caption("Values are simulated for demonstration and academic analysis purposes.")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("""
                    <div class="stat-box">
                        <div class="stat-number">1,240</div>
                        <div class="stat-label">Simulated Households (Demo)</div>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown("""
                    <div class="stat-box">
                        <div class="stat-number" style="color: #fca5a5;">35%</div>
                        <div class="stat-label">High Inflation Risk</div>
                    </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown("""
                    <div class="stat-box">
                        <div class="stat-number" style="color: #86efac;">12</div>
                        <div class="stat-label">Active Policy Alerts</div>
                    </div>
                """, unsafe_allow_html=True)
                
            st.markdown("<br>", unsafe_allow_html=True)
            
            # ACTION ACTIONS
            st.markdown("### ⚡ Quick Actions")
            ac1, ac2, ac3, ac4 = st.columns(4)
            
            with ac1:
                st.markdown("""
                    <div class="action-box">
                        <div class="action-icon">📈</div>
                        <div class="action-title">Policy Insights</div>
                        <div class="action-desc">Deep dive into inflation trends</div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("Open Insights", key="btn_insights", use_container_width=True):
                    st.session_state.pm_page = "Policy Insights"
                    st.rerun()
                    
            with ac2:
                 st.markdown("""
                    <div class="action-box">
                        <div class="action-icon">🚨</div>
                        <div class="action-title">Risk Monitor</div>
                        <div class="action-desc">View high-risk demographic heatmaps</div>
                    </div>
                """, unsafe_allow_html=True)
                 if st.button("View Heatmaps", key="btn_risk", use_container_width=True):
                    st.session_state.pm_page = "Policy Insights" # Mapping to existing page
                    st.rerun()

            with ac3:
                 st.markdown("""
                    <div class="action-box">
                        <div class="action-icon">📞</div>
                        <div class="action-title">Contact Citizens</div>
                        <div class="action-desc">Send alerts to affected groups</div>
                    </div>
                """, unsafe_allow_html=True)
                 if st.button("Contact Tools", key="btn_contact", use_container_width=True):
                    st.session_state.pm_page = "Contact Users"
                    st.rerun()

            with ac4:
                 st.markdown("""
                    <div class="action-box">
                        <div class="action-icon">📑</div>
                        <div class="action-title">Generate Report</div>
                        <div class="action-desc">Download PDF summary of status</div>
                    </div>
                """, unsafe_allow_html=True)
                 st.button("Download PDF", key="btn_pdf", use_container_width=True) # Placeholder action

            # Footer
            st.markdown("<br><hr><div style='text-align:center; color:#64748b; font-size:0.8rem;'>Policy Maker Control Panel – HIEI System v1.0</div>", unsafe_allow_html=True)

        elif menu == "Policy Insights":
            display_policy_dashboard()
        elif menu == "Contact Users":
            from views.policy_dashboard import display_contact_users
            display_contact_users()
        elif menu == "Logout":
            logout()
            
    else:
        # PUBLIC / GUEST MODE
        # State-based navigation for Guest Mode
        if "guest_page" not in st.session_state:
            st.session_state.guest_page = "Home"

        nav_options = [
            "Home",
            "User Login",
            "User Register",
            "Policy Maker Login",
            "Policy Maker Register"
        ]

        try:
            # Sync sidebar with state
            current_index = nav_options.index(st.session_state.guest_page)
        except ValueError:
            current_index = 0

        menu = st.sidebar.radio("Menu", nav_options, index=current_index)

        # Update state if sidebar clicked
        if menu != st.session_state.guest_page:
            st.session_state.guest_page = menu
            st.rerun()

        if menu == "Home":
            # Load Professional CSS
            import os
            css_path = os.path.join(os.path.dirname(__file__), 'assets', 'style.css')
            with open(css_path) as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

            # --- HERO SECTION ---
            st.markdown("""
                <div class="hero-container">
                    <div class="hero-title">HIEI SYSTEM</div>
                    <div class="hero-subtitle">Household Inflation Effect Index</div>
                    <div class="hero-divider"></div>
                    <p style="font-size: 1.1rem; color: #cbd5e1; max_width: 600px; margin: 0 auto;">
                        An advanced analytics platform to simulate inflation impact on household expenses 
                        and support data-driven policy decisions.
                    </p>
                </div>
            """, unsafe_allow_html=True)

            # --- ROLE BASED ACCESS CARDS ---
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("""
                    <div class="role-card-container">
                        <div class="role-icon">👤</div>
                        <div class="role-title">Citizen User</div>
                        <div class="role-desc">
                            Track your personal inflation rate, simulate future expenses, 
                            and get AI-driven investment advice.
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                # Buttons outside HTML to function correctly
                c1, c2 = st.columns(2)
                if c1.button("Login as Citizen", type="primary", use_container_width=True):
                    st.session_state.guest_page = "User Login"
                    st.rerun()
                if c2.button("Register as Citizen", use_container_width=True):
                    st.session_state.guest_page = "User Register"
                    st.rerun()

            with col2:
                st.markdown("""
                    <div class="role-card-container">
                        <div class="role-icon">🏛️</div>
                        <div class="role-title">Policy Maker</div>
                        <div class="role-desc">
                            Monitor economic stress across demographics, analyze risk heatmaps, 
                            and formulate targeted welfare policies.
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                c3, c4 = st.columns(2)
                if c3.button("Login as Admin", type="primary", use_container_width=True):
                    st.session_state.guest_page = "Policy Maker Login"
                    st.rerun()
                if c4.button("Register as Admin", use_container_width=True):
                    st.session_state.guest_page = "Policy Maker Register"
                    st.rerun()

            # --- SYSTEM HIGHLIGHTS ---
            st.markdown("""
                <div class="highlights-strip">
                    <div class="highlight-item">⚡ Real-time Analysis</div>
                    <div class="highlight-item">🔒 Secure Platform</div>
                    <div class="highlight-item">📊 AI Forecasting</div>
                    <div class="highlight-item">📑 Policy Reports</div>
                </div>
            """, unsafe_allow_html=True)

            # --- FEATURES OVERVIEW ---
            st.markdown("### Core Capabilities")
            f1, f2, f3, f4 = st.columns(4)
            
            with f1:
                st.markdown("""
                    <div class="feature-card">
                        <div class="feature-title">Inflation Simulator</div>
                        <div class="feature-text">Predict future costs of food, fuel, and healthcare based on your localized data.</div>
                    </div>
                """, unsafe_allow_html=True)
            with f2:
                st.markdown("""
                    <div class="feature-card">
                        <div class="feature-title">Budget Analysis</div>
                        <div class="feature-text">Analyze monthly spending patterns to identify critical financial stress points.</div>
                    </div>
                """, unsafe_allow_html=True)
            with f3:
                st.markdown("""
                    <div class="feature-card">
                        <div class="feature-title">Policy Insights</div>
                        <div class="feature-text">Executive dashboards for administrators to monitor demographic economic health.</div>
                    </div>
                """, unsafe_allow_html=True)
            with f4:
                st.markdown("""
                    <div class="feature-card">
                        <div class="feature-title">Smart Advisory</div>
                        <div class="feature-text">Get personalized recommendations for insurance and savings to mitigation inflation.</div>
                    </div>
                """, unsafe_allow_html=True)

            # --- FOOTER ---
            st.markdown("""
                <div class="footer">
                    &copy; 2025 HIEI System. All Rights Reserved. <br>
                    Designed for Academic & Policy Research Purposes.
                </div>
            """, unsafe_allow_html=True)
        elif menu == "User Login":
            user_login()
        elif menu == "User Register":
            user_register()
        elif menu == "Policy Maker Login":
            policy_login()
        elif menu == "Policy Maker Register":
            policy_register()
            


if __name__ == "__main__":
    main()
