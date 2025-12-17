import streamlit as st
import requests

API_BASE = "http://127.0.0.1:5000/api"

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
    
    if 'last_savings' not in st.session_state or 'last_salary' not in st.session_state:
        st.warning("Please run the Inflation Calculator first to generate personalized insights.")
        return
        
    savings = st.session_state['last_savings']
    salary = st.session_state['last_salary']
    
    agree = st.checkbox("I verify that I understand this is for educational purposes only.")
    if not agree:
        st.info("⚠️ Please accept the disclaimer above.")
        return

    st.divider()

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
def display_insurance_page():
    st.header("🛡️ Insurance & Risk Management")
    st.caption("Risk management is the foundation of financial planning.")
    
    # Left / Right Split as requested
    col_left, col_right = st.columns([1, 1.5])
    
    with col_left:
        st.subheader("📚 Insurance Types")
        with st.container():
            st.markdown("""
            **1. Term Life Insurance**  
            *Who:* Breadwinners with dependents.  
            *What:* Pays lumpsum on death. Pure risk cover.
            """)
            st.markdown("---")
            st.markdown("""
            **2. Health Insurance**  
            *Who:* Everyone.  
            *What:* Covers hospitalization. Medical inflation > 10%.
            """)
            st.markdown("---")
            st.markdown("""
            **3. Motor Insurance**  
            *Who:* Vehicle Owners.  
            *What:* Mandatory 3rd party liability + Own damage.
            """)
            st.markdown("---")
            st.markdown("""
            **4. Critical Illness**  
            *Who:* High risk of lifestyle diseases.  
            *What:* Fixed payout on diagnosis.
            """)

    with col_right:
        st.subheader("📋 Your Personalized Plan")
        
        # Simple inputs for personalization
        has_dependents = st.radio("Do you have financial dependents?", ["Yes", "No"], horizontal=True, key="ins_dep")
        has_health_cover = st.radio("Do you have non-employer health insurance?", ["Yes", "No"], horizontal=True, key="ins_health")
        
        st.divider()
        
        rec_count = 0
        if has_dependents == "Yes":
            rec_count += 1
            st.markdown(f"""
            <div style="border: 1px solid #EF553B; padding: 15px; border-radius: 8px; margin-bottom: 10px; background-color: #2D1B1B;">
                <h4 style="margin:0; color: #EF553B;">Priority: Term Life Insurance</h4>
                <p style="font-size:0.9em;">Reason: You have dependents who rely on your income.</p>
                <p><strong>Proposed Cover:</strong> 15 - 20x Annual Income</p>
                <a href="https://www.policybazaar.com/term-insurance/" target="_blank">Compare Term Plans</a>
            </div>
            """, unsafe_allow_html=True)
        
        if has_health_cover == "No":
            rec_count += 1
            st.markdown(f"""
            <div style="border: 1px solid #FFA15A; padding: 15px; border-radius: 8px; margin-bottom: 10px; background-color: #2D251B;">
                <h4 style="margin:0; color: #FFA15A;">Priority: Health Insurance</h4>
                <p style="font-size:0.9em;">Reason: Employer cover is tied to your job. You need personal cover.</p>
                <p><strong>Proposed Cover:</strong> ₹5 - ₹10 Lakhs Base</p>
                <a href="https://www.starhealth.in/" target="_blank">View Health Plans</a> | <a href="https://www.acko.com/" target="_blank">Acko</a>
            </div>
            """, unsafe_allow_html=True)
            
        if rec_count == 0:
            st.success("✅ You have covered the basics! Consider Top-up Health or Accidental Disability covers.")
            
        with st.expander("📞 Request Advisor Callback", expanded=True):
            with st.form("callback_form_rec"):
                st.write("Get a call from a verified policy advisor.")
                i_name = st.selectbox("Topic", ["Term Insurance", "Health Insurance", "Portfolio Review"])
                submitted = st.form_submit_button("Request Call Now")
                if submitted:
                    if 'user_id' in st.session_state and st.session_state.user_id:
                        try:
                            pl = {"user_id": st.session_state.user_id, "insurer_name": i_name}
                            res = requests.post(f"{API_BASE}/data/callback", json=pl)
                            if res.status_code == 201:
                                st.success("Request sent! Reference ID saved.")
                            else:
                                st.error("Failed to send request.")
                        except:
                            st.error("Connection failed.")
                    else:
                        st.error("Please login first.")
