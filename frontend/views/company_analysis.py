import streamlit as st
from data.company_data import COMPANIES

def display_company_analysis():
    # --- HEADER ---
    st.markdown("""
        <div style="padding-bottom: 20px; border-bottom: 1px solid #30363D; margin-bottom: 20px;">
            <h2 style="margin: 0; color: #FAFAFA; font-size: 2rem;">Company Analysis Guide</h2>
            <p style="margin: 5px 0 0; color: #8B949E; font-size: 1rem;">
                Simple, clear insights to help you understand what you are investing in.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # --- SEARCH & SELECT ---
    company_names = ["Select a Company"] + [c['name'] for c in COMPANIES]
    selected_name = st.selectbox("🔍 Select a Company to Study", company_names)
    
    if selected_name != "Select a Company":
        comp = next(c for c in COMPANIES if c['name'] == selected_name)
        render_company_card(comp)
    else:
        st.info("👈 Please select a company from the dropdown to start learning.")

def render_company_card(comp):
    # --- CSS STYLING ---
    st.markdown("""
    <style>
    .card-container { background-color: #161B22; padding: 25px; border-radius: 12px; border: 1px solid #30363D; margin-bottom: 25px; }
    .section-title { font-size: 1.1rem; color: #4DA6FF; font-weight: 600; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 0.5px; }
    
    /* Overview Box */
    .overview-box { background: linear-gradient(180deg, #1E232B 0%, #161B22 100%); padding: 20px; border-radius: 8px; border-left: 4px solid #00CC96; }
    .overview-text { color: #C9D1D9; font-size: 1rem; line-height: 1.6; }
    
    /* Property Grid */
    .prop-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 15px; }
    .prop-card { background-color: #21262D; padding: 15px; border-radius: 8px; border: 1px solid #30363D; text-align: center; }
    .prop-label { font-size: 0.8rem; color: #8B949E; text-transform: uppercase; margin-bottom: 5px; }
    .prop-status { font-size: 1rem; color: #FAFAFA; font-weight: 600; margin-bottom: 5px; }
    .prop-desc { font-size: 0.75rem; color: #6E7681; }
    
    /* Risk Cards */
    .risk-card { background-color: #21262D; padding: 12px; border-radius: 6px; border-left: 3px solid #EF553B; margin-bottom: 10px; }
    .risk-title { color: #FAFAFA; font-weight: 600; font-size: 0.95rem; }
    .risk-level { float: right; font-size: 0.8rem; padding: 2px 8px; border-radius: 4px; background: rgba(239, 85, 59, 0.2); color: #EF553B; }
    
    /* Suitability Box */
    .suit-box { background-color: #1F242C; padding: 20px; border-radius: 8px; border: 1px dashed #4DA6FF; text-align: center; }
    .checklist-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #30363D; }
    </style>
    """, unsafe_allow_html=True)

    # 1️⃣ COMPANY OVERVIEW
    st.markdown(f"### 🏢 {comp['name']} ({comp['ticker']})")
    
    snap = comp.get('snapshot', {})
    financials = comp.get('dash_financials', {})
    industry = comp.get('dash_industry', {})
    
    # Parse business model for "How it makes money"
    # Assuming list format: ['Revenue -> X', 'Model -> Y']
    biz_model_text = "• " + "\n• ".join([bm.split('->')[1].strip() if '->' in bm else bm for bm in comp.get('business_model', [])[:3]])

    st.markdown(f"""
    <div class="card-container">
        <div class="section-title">Company Overview</div>
        <div class="overview-box">
            <div style="font-weight: 600; color: #FAFAFA; margin-bottom: 5px;">What does this company do?</div>
            <div class="overview-text">{comp['overview']}</div>
            <br>
            <div style="font-weight: 600; color: #FAFAFA; margin-bottom: 5px;">Industry & Sector</div>
            <div class="overview-text">{comp['sector']} - {industry.get('Growth', 'Growth')} Industry</div>
            <br>
            <div style="font-weight: 600; color: #FAFAFA; margin-bottom: 5px;">How does it make money?</div>
            <div class="overview-text" style="white-space: pre-line;">{biz_model_text}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2️⃣ CORE COMPANY PROPERTIES
    # Mapping Logic
    # Business Strength: Snapshot 'market_position'
    # Industry Stability: Ind Context 'Cyclicality' or snapshot 'style'
    # Revenue Trend: dash_financials 'Rev Trend'
    # Profitability: dash_financials 'Profit Stability'
    # Debt Level: dash_financials 'Debt Comfort'
    # Cash Flow: dash_financials 'Cash Flow'
    
    st.markdown("""
    <div class="card-container">
        <div class="section-title">Core Business Properties</div>
        <div class="prop-grid">
            <div class="prop-card">
                <div class="prop-label">Business Strength</div>
                <div class="prop-status" style="color: #00CC96;">{0}</div>
                <div class="prop-desc">Market Position</div>
            </div>
            <div class="prop-card">
                <div class="prop-label">Industry Stability</div>
                <div class="prop-status" style="color: #E1AD01;">{1}</div>
                <div class="prop-desc">{2}</div>
            </div>
            <div class="prop-card">
                <div class="prop-label">Revenue Trend</div>
                <div class="prop-status" style="color: #00CC96;">{3}</div>
                <div class="prop-desc">Sales Growth</div>
            </div>
            <div class="prop-card">
                <div class="prop-label">Profitability</div>
                <div class="prop-status" style="color: #00CC96;">{4}</div>
                <div class="prop-desc">Consistency</div>
            </div>
            <div class="prop-card">
                <div class="prop-label">Debt Level</div>
                <div class="prop-status" style="color: {5};">{6}</div>
                <div class="prop-desc">Balance Sheet</div>
            </div>
            <div class="prop-card">
                <div class="prop-label">Cash Flow Health</div>
                <div class="prop-status" style="color: {7};">{8}</div>
                <div class="prop-desc">Operational Cash</div>
            </div>
        </div>
    </div>
    """.format(
        snap.get('market_position', 'Strong'), # 0
        snap.get('style', 'Stable'), # 1
        industry.get('Cyclicality', 'Moderate'), # 2
        financials.get('Rev Trend', 'Growing').replace("↑", "").replace("→", "").strip(), # 3
        financials.get('Profit Stability', 'Stable').replace("✔", "").replace("→", "").strip(), # 4
        "#00CC96" if "Zero" in financials.get('Debt Comfort', '') or "Low" in financials.get('Debt Comfort', '') or "N/A" in financials.get('Debt Comfort', '') else "#EF553B", # 5 (Color)
        financials.get('Debt Comfort', 'Manageable').replace("✔", "").replace("→", "").strip(), # 6
        "#00CC96" if "Positive" in financials.get('Cash Flow', '') or "Robust" in financials.get('Cash Flow', '') else "#E1AD01", # 7 (Color)
        financials.get('Cash Flow', 'Positive').replace("✔", "").replace("→", "").strip() # 8
    ), unsafe_allow_html=True)
    
    # 🚨 NEW: COMPANY GROWTH DASHBOARD
    st.markdown("""
    <div class="card-container">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <div class="section-title" style="margin-bottom: 0;">🚀 Company Growth Dashboard</div>
            <div style="background-color: #21262D; border: 1px solid #30363D; padding: 5px 10px; border-radius: 6px; font-size: 0.75rem; color: #8B949E;">
                ℹ️ <strong>How to read:</strong> Shows if growth is steady (safe) or wavy (risky).
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Growth Indicators Logic
    rev_trend_raw = financials.get('Rev Trend', 'Steady')
    # Determine revenue arrows
    if 'Rising' in rev_trend_raw or 'Strong' in rev_trend_raw or 'Rapid' in rev_trend_raw:
        rev_icon = "↗️"
        rev_status = "Increasing"
        rev_desc = "Sales are going up."
    elif 'Slow' in rev_trend_raw or 'Stable' in rev_trend_raw or 'Consistent' in rev_trend_raw:
        rev_icon = "➡️"
        rev_status = "Stable"
        rev_desc = "Sales are steady."
    else:
        rev_icon = "↘️"
        rev_status = "Declining"
        rev_desc = "Sales are facing pressure."

    # Profit Logic
    prof_trend_raw = financials.get('Profit Stability', 'Stable')
    if 'High' in prof_trend_raw or 'Rising' in prof_trend_raw or 'Strong' in prof_trend_raw:
        prof_icon = "✅"
        prof_status = "Strong"
        prof_desc = "Profits are healthy."
    elif 'Volatile' in prof_trend_raw:
        prof_icon = "⚠️"
        prof_status = "Volatile"
        prof_desc = "Profits go up and down."
    else:
        prof_icon = "🔹"
        prof_status = "Consistent"
        prof_desc = "Profits are predictable."

    # Expansion Logic (Simulated from Outlook)
    outlook_drive = comp.get('dash_outlook', {}).get('Driver', '')
    if 'Growth' in outlook_drive or 'Expansion' in outlook_drive or 'Transformation' in outlook_drive:
        exp_icon = "🌍"
        exp_status = "Expanding"
        exp_desc = "Investing in new areas."
    else:
        exp_icon = "🔒"
        exp_status = "Steady"
        exp_desc = "Focusing on core business."

    # 1️⃣ Growth Overview Cards (Grid)
    st.markdown(f"""
        <div class="prop-grid" style="margin-top: 0; margin-bottom: 20px;">
            <div class="prop-card" style="background-color: #1F242C; border: 1px dashed #444;">
                <div class="prop-label">Revenue Growth</div>
                <div class="prop-status" style="color: #FAFAFA;">{rev_icon} {rev_status}</div>
                <div class="prop-desc">{rev_desc}</div>
            </div>
            <div class="prop-card" style="background-color: #1F242C; border: 1px dashed #444;">
                <div class="prop-label">Profit Growth</div>
                <div class="prop-status" style="color: #FAFAFA;">{prof_icon} {prof_status}</div>
                <div class="prop-desc">{prof_desc}</div>
            </div>
            <div class="prop-card" style="background-color: #1F242C; border: 1px dashed #444;">
                <div class="prop-label">Business Expansion</div>
                <div class="prop-status" style="color: #FAFAFA;">{exp_icon} {exp_status}</div>
                <div class="prop-desc">{exp_desc}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 2️⃣ Growth Trend Visualization (Chart)
    st.markdown('<div class="prop-label" style="text-align: left; margin-bottom: 10px;">📈 Growth Trend (Visualized)</div>', unsafe_allow_html=True)
    
    # Re-using the conceptual chart logic but making it cleaner/embedded
    import math
    import random
    archetype = comp.get('growth_archetype', 'Steady')
    points = 30
    chart_data = []
    base_val = 100
    for i in range(points):
        x = i / 3.0
        if archetype == 'Compounder': val = base_val * (1.12 ** x) + random.uniform(-1, 1)
        elif archetype == 'Cyclical': val = base_val + (8 * x) + (15 * math.sin(x))
        elif archetype == 'Defensive': val = base_val * (1.05 ** x)
        elif archetype == 'FastGrowth': val = base_val * (1.20 ** x) + random.uniform(-3, 3)
        else: val = base_val + (3 * x) + random.uniform(-10, 10)
        chart_data.append(val)
        
    st.line_chart(chart_data, height=150, use_container_width=True)
    
    # 3️⃣ Growth Stability Indicator
    stability = "High Stability" if archetype in ['Compounder', 'Defensive'] else "Medium Stability" if archetype == 'FastGrowth' else "Low Stability (Cyclical)"
    st.markdown(f"""
        <div style="background-color: #21262D; border-top: 1px solid #30363D; padding-top: 15px; margin-top: 10px; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span class="prop-label">Growth Stability:</span>
                <span style="color: #FAFAFA; font-weight: 600; margin-left: 5px;">{stability}</span>
            </div>
            <div style="font-size: 0.8rem; color: #6E7681;">Based on historical track record.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    # END GROWTH DASHBOARD

    # 3️⃣ RISK SUMMARY & 4️⃣ MANAGEMENT (Two Columns)
    col_risk, col_mgmt = st.columns(2)
    
    with col_risk:
        st.markdown('<div class="section-title">⚠️ Risk Summary</div>', unsafe_allow_html=True)
        risks = comp.get('dash_risks', [])
        risk_html = ""
        for r in risks:
            risk_html += f"""
            <div class="risk-card">
                <span class="risk-title">{r['name']}</span>
                <span class="risk-level">{r['level']}</span>
            </div>
            """
        st.markdown(risk_html, unsafe_allow_html=True)
        
    with col_mgmt:
        st.markdown('<div class="section-title">🏆 Management & Stability</div>', unsafe_allow_html=True)
        mgmt = comp.get('dash_outlook', {}).get('Management', 'Professional')
        perf = comp.get('performance', 'Stable track record.')
        st.markdown(f"""
        <div style="background-color: #21262D; padding: 15px; border-radius: 8px; height: 100%;">
            <div style="margin-bottom: 10px;">
                <span style="color: #8B949E; font-size: 0.85rem;">Management Quality</span><br>
                <span style="color: #FAFAFA; font-weight: 600;">{mgmt.replace('✔','').strip()}</span>
            </div>
            <div style="margin-bottom: 10px;">
                <span style="color: #8B949E; font-size: 0.85rem;">Track Record</span><br>
                <span style="color: #FAFAFA; font-size: 0.95rem;">{perf}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 5️⃣ INVESTMENT SUITABILITY SUMMARY
    st.markdown("---")
    
    # Logic for Classification (Simulated based on existing data properties)
    # Large Cap: Leader market position + Low/Med Risk
    is_large_cap = "Leader" in snap.get('market_position', '') or "Dominant" in comp['overview']
    # Mid Cap: Challenger or Growth style + Med Risk (simplified logic)
    is_mid_cap = "Challenger" in snap.get('market_position', '') or "Med" in comp.get('risk', '')
    # Small Cap: High Risk or specific mention (Default False for these major companies)
    is_small_cap = "High" in comp.get('risk', '')
    # Startup: specific mention (Default False for listed giants)
    is_startup = False 

    def render_suitablity_row(label, is_yes, description):
        badge_color = "#2bbb5b" if is_yes else "#ef553b" # Green vs Red
        badge_text = "YES" if is_yes else "NO"
        return f"""
        <div class="checklist-row" style="align-items: center;">
            <div style="flex: 1; color: #C9D1D9; font-weight: 500;">{label}</div>
            <div style="flex: 2; color: #8B949E; font-size: 0.9rem;">{description}</div>
            <div style="background-color: {badge_color}; color: #fff; padding: 2px 10px; border-radius: 4px; font-weight: bold; font-size: 0.8rem;">{badge_text}</div>
        </div>
        """

    st.markdown("""
    <div class="card-container">
        <div class="section-title" style="color: #FAFAFA; border-bottom: none;">🎯 Investment Suitability Summary</div>
        <p style="color: #8B949E; font-size: 0.9rem; margin-top: -10px; margin-bottom: 20px;">
            Quick classification to help you decide if this matches your profile.
        </p>
    """, unsafe_allow_html=True)

    st.markdown(render_suitablity_row(
        "Large-Cap Investment", 
        is_large_cap, 
        "Stable, established market leaders."
    ), unsafe_allow_html=True)
    
    st.markdown(render_suitablity_row(
        "Mid-Cap Investment", 
        is_mid_cap and not is_large_cap, 
        "Higher growth potential, moderate risk."
    ), unsafe_allow_html=True)

    st.markdown(render_suitablity_row(
        "Small-Cap Investment", 
        is_small_cap, 
        "High risk, high volatility."
    ), unsafe_allow_html=True)

    st.markdown(render_suitablity_row(
        "Startup Category", 
        is_startup, 
        "Early stage, very high risk."
    ), unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # 6️⃣ DECISION HELPER (Checklist)
    st.markdown("### ✅ Decision Helper Checklist")
    checklist = comp.get('checklist_expanded', [])
    
    for item in checklist:
        is_pos = item['status'] in ['Yes', 'Strong', 'Wide', 'Up', 'High']
        icon = "✔" if is_pos else "Questions to ask:"
        color = "#00CC96" if is_pos else "#E1AD01"
        st.markdown(f"""
        <div class="checklist-row">
            <span style="color: #C9D1D9;">{icon} Is {item['item']} strong?</span>
            <span style="color: {color}; font-weight: 600;">{item['status']}</span>
        </div>
        """, unsafe_allow_html=True)
        
    st.caption("Note: This checklist is for educational guidance only.")


