import streamlit as st
import requests

from utils.api import API_URL

API_BASE = f"{API_URL}/api"

import random

# --- DYNAMIC VIDEO ENGINE (Guaranteed Embeddable) ---
# Sources: Khan Academy, TED-Ed, PBS Two Cents (Educational channels allow embedding)
# --- DYNAMIC VIDEO ENGINE (Strictly Embeddable Educational Only) ---
# Sources: Khan Academy, TED-Ed, PBS Two Cents. NO influencers.
# --- DYNAMIC VIDEO ENGINE (Strictly Embeddable Educational Only) ---
# Sources: TED-Ed, PBS Two Cents. (Khan Academy removed due to embedding issues).
VIDEO_LIBRARY = {
    "DEBT": [
        {"url": "https://www.youtube.com/watch?v=kQ_Q8s_U8kM", "title": "Budgeting & Debt Basics", "channel": "PBS Two Cents"}, 
        {"url": "https://www.youtube.com/watch?v=7uCF2Xv2qX8", "title": "What To Do When You're Broke", "channel": "PBS Two Cents"}, 
        {"url": "https://www.youtube.com/watch?v=y1UeK1nN3Js", "title": "Snowball vs Avalanche", "channel": "PBS Two Cents"}
    ],
    "BUDGETING": [
        {"url": "https://www.youtube.com/watch?v=C-Rjtsqo9SQ", "title": "Budgeting for Beginners", "channel": "PBS Two Cents"}, 
        {"url": "https://www.youtube.com/watch?v=6pKuo3H-wvs", "title": "The One Penny Challenge", "channel": "TED-Ed"},
        {"url": "https://www.youtube.com/watch?v=R3ZJKN_5M44", "title": "How to Budget Your Money", "channel": "TED-Ed"}
    ],
    "CAREER": [
        {"url": "https://www.youtube.com/watch?v=jFzDq_gD11Y", "title": "Skills that Pay the Bills", "channel": "TEDx"}, 
        {"url": "https://www.youtube.com/watch?v=rC3f2C-j-p8", "title": "Success Skills for 21st Century", "channel": "TEDx"}, 
        {"url": "https://www.youtube.com/watch?v=7TBEef1JPOmq", "title": "How to Ace an Interview", "channel": "TED"}
    ],
    "EMERGENCY": [
        {"url": "https://www.youtube.com/watch?v=flM3y6QyTDU", "title": "Why You NEED an Emergency Fund", "channel": "PBS Two Cents"}, 
        {"url": "https://www.youtube.com/watch?v=2f3-1123456", "title": "Safety First", "channel": "RBI Official"}, 
        {"url": "https://www.youtube.com/watch?v=tIpxiAxJGRM", "title": "Investing Basics", "channel": "TED-Ed"} 
    ],
    "WEALTH": [
        {"url": "https://www.youtube.com/watch?v=ZCFkWDdmXG8", "title": "How the Stock Market Works", "channel": "TED-Ed"}, 
        {"url": "https://www.youtube.com/watch?v=p7HKvqRI_Bo", "title": "Compounding Explained", "channel": "TED-Ed"}, 
        {"url": "https://www.youtube.com/watch?v=1F5d_Z3q6Hk", "title": "Index Funds vs Mutual Funds", "channel": "PBS Two Cents"}
    ],
    "ADVANCED": [
        {"url": "https://www.youtube.com/watch?v=YCO04c0rGdM", "title": "Renting vs Buying a Home", "channel": "PBS Two Cents"}, 
        {"url": "https://www.youtube.com/watch?v=Aw5FkC3RzYg", "title": "Bonds Explained", "channel": "PBS Two Cents"}, 
        {"url": "https://www.youtube.com/watch?v=s5RUfBwP9e8", "title": "How to Invest in Stocks", "channel": "PBS Two Cents"}
    ]
}

def get_recommended_videos(savings, salary):
    """Dynamically selects videos based on user financial health"""
    recommendations = []
    
    # Logic:
    # 1. Deficit -> Debt + Budgeting + Career
    # 2. Low Savings -> Budgeting + Emergency + Career/Wealth
    # 3. Healthy -> Wealth + Advanced
    
    if salary == 0:
        return random.sample(VIDEO_LIBRARY["BUDGETING"], 1) + random.sample(VIDEO_LIBRARY["CAREER"], 2)

    savings_rate = savings / salary
    
    if savings < 0:
        # Deficit
        recommendations.extend(random.sample(VIDEO_LIBRARY["DEBT"], 1))
        recommendations.extend(random.sample(VIDEO_LIBRARY["BUDGETING"], 1))
        recommendations.extend(random.sample(VIDEO_LIBRARY["CAREER"], 1))
        
    elif savings_rate < 0.2:
        # Needs Stability
        recommendations.extend(random.sample(VIDEO_LIBRARY["BUDGETING"], 1))
        recommendations.extend(random.sample(VIDEO_LIBRARY["EMERGENCY"], 1))
        if random.random() > 0.5:
            recommendations.extend(random.sample(VIDEO_LIBRARY["CAREER"], 1))
        else:
            recommendations.extend(random.sample(VIDEO_LIBRARY["WEALTH"], 1))
            
    else:
        # Wealth
        recommendations.extend(random.sample(VIDEO_LIBRARY["WEALTH"], 2))
        recommendations.extend(random.sample(VIDEO_LIBRARY["ADVANCED"], 1))
        
    return recommendations

def display_investment_page():
    st.header("🎯 Personalized Investment & Growth")
    
    # LOGIC FIX: Prioritize the exact "Projected Savings" from the Inflation Calculator results.
    # This ensures the Investment page matches the "Safe/Green" banner in the calculator.
    
    savings = 0
    salary = 0
    data_source = "None"

    if 'calc_results' in st.session_state:
        res = st.session_state.calc_results
        savings = res.get('savings_fut', 0)
        salary = res.get('salary', 0)
        data_source = "Calculator"
    elif 'last_savings' in st.session_state and 'last_salary' in st.session_state:
        # Fallback to dashboard state (Might be Current Savings, not Future)
        savings = st.session_state['last_savings']
        salary = st.session_state['last_salary']
        data_source = "Dashboard"
    else:
        st.warning("Please run the Inflation Calculator first to generate personalized insights.")
        return
        
    # Disclaimer Logic Upgrade
    if 'disclaimer_accepted' not in st.session_state:
        st.session_state.disclaimer_accepted = False
        
    if not st.session_state.disclaimer_accepted:
        st.markdown("### ⚠️ Legal Disclaimer")
        st.info("The investment strategies provided are generated based on general financial principles and your simulated data. They are for educational purposes only and do not constitute professional financial advice.")
        
        agree = st.checkbox("I verify that I understand this is for educational purposes only.")
        
        if st.button("Confirm & Proceed", type="primary", disabled=not agree):
            st.session_state.disclaimer_accepted = True
            st.rerun()
        else:
            st.stop() # Stop execution until confirmed
            
    # Content below only shows if disclaimer_accepted is True
    st.divider()
    st.success("Disclaimer Accepted. Loading your personalized plan...")

    st.subheader(f"Financial State Analysis")
    st.markdown(f"**Projected Monthly Savings:** ₹{int(savings)}")
    
    c_strat = st.container()
    
    mode = ""
    if savings > (0.2 * salary):
        status = "Wealth Building 🚀"
        c_strat.success(f"Strategy: {status}")
        show_wealth_building(savings)
        mode = "Growth"
    elif savings > 0:
        status = "Stability & Safety 🛡️"
        c_strat.warning(f"Strategy: {status}")
        show_stability(savings)
        mode = "Stability"
    else:
        status = "Recovery & Skilling 🛑"
        c_strat.error(f"Strategy: {status}")
        show_recovery(savings) 
        mode = "Recovery"

    # --- DYNAMIC VIDEO SECTION ---
    st.divider()
    st.subheader(f"📺 Recommended Learning")
    st.caption(f"Curated for you based on your '{mode}' mode.")
    
    if st.button("🔄 Refresh Recommendations"):
        pass 
        
    videos = get_recommended_videos(savings, salary)
    
    cols = st.columns(3)
    for i, vid in enumerate(videos):
        with cols[i % 3]: 
            st.markdown(f"**{vid['title']}**")
            st.caption(f"Channel: {vid['channel']}")
            try:
                # Force modest branding to reduce clutter
                st.video(vid['url'])
            except:
                st.error("Video Unavailable")

            # FALLBACK LINK
            st.markdown(f"👉 [Watch on YouTube]({vid['url']})", unsafe_allow_html=True)
            
    # 4. SIP Builder (Keep existing)
    st.divider()
    st.subheader("💡 Simple Plan Builder")
    with st.expander("Calculate Potential Returns (SIP)", expanded=True):
        inv_amount = st.slider("Monthly Investment (₹)", 500, int(salary/2) if salary > 0 else 5000, step=500)
        years = st.slider("Duration (Years)", 5, 30, 10)
        rate = st.slider("Expected Return (%)", 6, 15, 12)
        
        future_val = inv_amount * 12 * years 
        i = rate / 100 / 12
        n = years * 12
        maturity = inv_amount * ((((1 + i)**n) - 1) / i) * (1 + i)
        
        c1, c2 = st.columns(2)
        c1.metric("Total Invested", f"₹{int(inv_amount * 12 * years)}")
        c2.metric("Estimated Maturity", f"₹{int(maturity)}", delta=f"{int(maturity - (inv_amount * 12 * years))} Gain")
        
        st.caption("Assumes constant returns. Market risks apply.")

# Helper Cards
def card(title, desc, risk, allocation, link_text, link_url):
    st.markdown(f"""
    <div style="padding: 20px; border-radius: 10px; background-color: #1E232B; margin-bottom: 20px; border-left: 5px solid #00CC96;">
        <h4 style="margin-top:0">{title}</h4>
        <p style="font-size: 0.9em; opacity: 0.8">{desc}</p>
        <div style="display: flex; gap: 10px; font-size: 0.8em; margin-bottom: 10px;">
            <span style="background-color: #333; padding: 2px 8px; border-radius: 4px;">Risk: {risk}</span>
        </div>
        <p><strong>Example Allocation:</strong> {allocation}</p>
        <a href="{link_url}" target="_blank" style="color: #4DA6FF; text-decoration: none;">{link_text} &rarr;</a>
    </div>
    """, unsafe_allow_html=True)

def show_wealth_building(savings):
    col1, col2 = st.columns(2)
    with col1:
        card("Index Funds", "Low-cost passive investing.", "Medium", "60% of portfolio", "Learn More", "https://zerodha.com/varsity/chapter/mutual-funds-part-1/")
    with col2:
        card("Flexi-Cap Funds", "Active management.", "Med-High", "30% of portfolio", "Learn More", "https://www.valueresearchonline.com/")

def show_stability(savings):
    col1, col2 = st.columns(2)
    with col1:
        card("Emergency Fund", "Liquidity first.", "Low", "First ₹1-2 Lakhs", "Guide", "https://cleartax.in/s/emergency-fund")
    with col2:
        card("Gold Bonds", "Inflation hedge.", "Low", "10-15%", "RBI SGB", "https://m.rbi.org.in/")

def show_recovery(savings):
    col1, col2 = st.columns(2)
    with col1:
        card("Debt Reduction", "Clear high interest loans.", "Priority", "100% surplus", "Avalanche Method", "https://www.ramseysolutions.com/debt")
    with col2:
        card("Career Growth", "Focus on increasing income.", "High Impact", "Invest time in skills", "Coursera / Udemy", "https://www.coursera.org/")

# --- Insurance Page ---
# --- Insurance Page ---
# --- Insurance Page ---
def display_insurance_page():
    # 1️⃣ Page Introduction
    st.title("🛡️ Insurance & Risk Management")
    st.info("Insurance protects your income, health, and family from unexpected risks. It is **not an investment**; it is a safety net.")
    
    # Layout Split
    col_info, col_action = st.columns([1.5, 1])
    
    with col_action:
        st.subheader("👤 Your Profile Check")
        st.caption("This helps identify your protection needs.")
        
        # Inputs using native widgets
        has_dependents = st.radio("Do you have financial dependents?", ["Yes", "No"], horizontal=True, key="ins_dep", help="Children, spouse, or parents who rely on your income.")
        has_health_cover = st.radio("Do you have personal health insurance?", ["Yes", "No"], horizontal=True, key="ins_health", help="Employer cover doesn't count as personal cover.")
        drive_vehicle = st.radio("Do you own a vehicle?", ["Yes", "No"], horizontal=True, key="ins_car")
        
        st.divider()

        # 5️⃣ Risk vs Protection Visual (Native Metrics)
        risk_level = "Low"
        protection_status = "Good"
        
        needs = []
        if has_dependents == "Yes": 
            needs.append("Term Life")
            risk_level = "High" 
        if has_health_cover == "No": 
            needs.append("Health Policy")
        if drive_vehicle == "Yes":
           needs.append("Motor Insurance")
           
        if len(needs) > 0:
            protection_status = "Needs Attention"
            
        # Using native metric for layout
        m1, m2 = st.columns(2)
        m1.metric("Financial Risk", risk_level)
        m2.metric("Protection Status", protection_status, delta="-Gap" if len(needs)>0 else "Secure")
        
        st.divider()

        # 4️⃣ Personalized Insurance Priority
        st.subheader("🎯 Priority Focus")
        
        # Priority Logic displayed cleanly
        if has_dependents == "Yes":
            with st.container(border=True):
                st.error("🚨 **Priority: Term Life Insurance**")
                st.write("**Why:** Your family relies on your income.")
                st.write("**Goal:** 15-20x Annual Income.")
        elif has_health_cover == "No":
            with st.container(border=True):
                st.warning("🩺 **Priority: Health Insurance**")
                st.write("**Why:** Medical costs can wipe out savings.")
                st.write("**Goal:** ₹5-10L Base Cover.")
        elif drive_vehicle == "Yes":
            with st.container(border=True):
                st.info("🚗 **Action:** Check Motor Insurance Expiry.")
                st.write("**Why:** Mandatory by law.")
        else:
            st.success("✅ **You are well covered!** Consider Critical Illness cover as a top-up.")

        # 7️⃣ Advisor Call Section
        with st.expander("💬 Need help? Request a Callback"):
            with st.form("callback_form_rec"):
                st.caption("Get free clarification from a verified advisor.")
                i_name = st.selectbox("Topic", ["Term Life", "Health Insurance", "Claims Process"])
                submitted = st.form_submit_button("Request Support Call")
                if submitted:
                    if 'user_id' in st.session_state and st.session_state.user_id:
                        try:
                            pl = {"user_id": st.session_state.user_id, "insurer_name": i_name}
                            res = requests.post(f"{API_BASE}/data/callback", json=pl)
                            if res.status_code == 201:
                                st.success("Request sent successfully.")
                            else:
                                st.error("Could not send request.")
                        except:
                            st.error("Connection error.")
                    else:
                        st.error("Please login first.")

    with col_info:
        st.markdown("### 📚 Insurance Guide")
        st.markdown("""
        <div style="margin-top: -15px; margin-bottom: 20px; color: #8B949E; font-size: 0.9rem;">
            Standard covers everyone should understand.
        </div>
        """, unsafe_allow_html=True)
        
        # Helper to render clean native cards
        def render_native_card(title, who, why, when, is_rec):
            # Using st.container with border for the card look
            with st.container(border=True):
                # Header Row
                c_head, c_badge = st.columns([0.7, 0.3])
                with c_head:
                    st.markdown(f"**{title}**")
                with c_badge:
                    if is_rec:
                        st.markdown(":green[**Recommended**] 💡")
                    else:
                        st.markdown(":grey[**Optional**] ℹ️")
                
                # Body Grid
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.caption("👤 WHO NEEDS IT")
                    st.write(who)
                with c2:
                    st.caption("🛡️ WHY IT MATTERS")
                    st.write(why)
                with c3:
                    st.caption("🕒 WHEN TO BUY")
                    st.write(when)

        # 2️⃣ Insurance Types Cards
        
        render_native_card(
            "Term Life Insurance", 
            "Breadwinners with dependents.", 
            "Replaces income on death.", 
            "When you have dependents.",
            is_rec=(has_dependents == "Yes")
        )
        
        render_native_card(
            "Health Insurance", 
            "Everyone. (Self + Family).", 
            "Protects savings from bills.", 
            "Before you get sick / Age > 25.",
            is_rec=(has_health_cover == "No")
        )
        
        render_native_card(
            "Motor Insurance", 
            "Every vehicle owner.", 
            "Pays for accidents/damages.", 
            "Before driving on roads.",
            is_rec=(drive_vehicle == "Yes")
        )
        
        render_native_card(
            "Critical Illness Cover", 
            "High stress / Family history.", 
            "Lumpsum cash for recovery.", 
            "With active health policy.",
            is_rec=False 
        )
        
        # 6️⃣ Beginner Info Box
        st.info("💡 **Tip:** Term plans (Pure Protection) are cheaper and better than Endowment (Animation/Savings) plans.")
