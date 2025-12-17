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
        menu = st.sidebar.radio("Menu", [
            "User Dashboard",
            "Inflation Calculator",
            "Inflation Dashboard",
            "Investments",
            "Company Analysis",
            "Insurance Information",
            "Logout"
        ])
        
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
        menu = st.sidebar.radio("Menu", [
            "Policy Dashboard",
            "Policy Insights",
            "Contact Users",
            "Logout"
        ])
        
        if menu == "Policy Dashboard":
            st.title("Policy Maker Home")
            st.write("Welcome to the Policy Administration Area.")
        elif menu == "Policy Insights":
            display_policy_dashboard()
        elif menu == "Contact Users":
            from views.policy_dashboard import display_contact_users
            display_contact_users()
        elif menu == "Logout":
            logout()
            
    else:
        # PUBLIC / GUEST MODE
        menu = st.sidebar.radio("Menu", [
            "Home",
            "User Login",
            "User Register",
            "Policy Maker Login",
            "Policy Maker Register"
        ])
        
        if menu == "Home":
            st.title("Welcome to HIEI")
            st.markdown("### Household Inflation Effect Index System")
            st.info("Please login to continue.")
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
