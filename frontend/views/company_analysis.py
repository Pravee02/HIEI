import streamlit as st
from data.company_data import COMPANIES

def display_company_analysis():
    # --- HEADER ---
    st.title("📊 Educational Company Analysis")
    st.markdown("""
    **Objective:** Learn about business models, strengths, and risks of India's leading companies.
    
    <div style="padding: 15px; border: 1px solid #ffcc00; border-radius: 8px; background-color: #332b00; color: #ffeb3b; margin-bottom: 20px;">
        <strong>⚠️ IMPORTANT DISCLAIMER:</strong><br>
        This analysis is for <strong>EDUCATIONAL PURPOSES ONLY</strong> and does not constitute financial advice.
        Stock market investments are subject to market risks. Past performance does not guarantee future returns.
        Users should consult a SEBI-registered financial advisor before making any investment decisions.
        This platform does not recommend buying or selling any securities.
    </div>
    """, unsafe_allow_html=True)
    
    # --- SEARCH & SELECT ---
    company_names = ["Select a Company"] + [c['name'] for c in COMPANIES]
    selected_name = st.selectbox("🔍 Search for a Company", company_names)
    
    if selected_name != "Select a Company":
        # Find the company data
        comp = next(c for c in COMPANIES if c['name'] == selected_name)
        render_company_card(comp)
    else:
        st.info("👈 Please select a company from the dropdown to view its analysis.")

def render_company_card(comp):
    # CSS for cards
    st.markdown("""
    <style>
    .company-card { background-color: #1E232B; padding: 25px; border-radius: 12px; border: 1px solid #444; margin-top: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.4); }
    .risk-badge-low { background-color: #0f3d0f; color: #4caf50; padding: 4px 12px; border-radius: 6px; font-weight:bold; border: 1px solid #4caf50; }
    .risk-badge-med { background-color: #3d3d0f; color: #ffeb3b; padding: 4px 12px; border-radius: 6px; font-weight:bold; border: 1px solid #ffeb3b; }
    .risk-badge-high { background-color: #3d0f0f; color: #ff5252; padding: 4px 12px; border-radius: 6px; font-weight:bold; border: 1px solid #ff5252; }
    .section-head { color: #4DA6FF; font-size: 1.05em; font-weight: 600; margin-top: 25px; margin-bottom: 12px; border-left: 3px solid #4DA6FF; padding-left: 10px; text-transform:uppercase; letter-spacing:1px; }
    .sub-head { color: #888; font-size: 0.85em; text-transform: uppercase; margin-top: 10px; margin-bottom: 5px; font-weight: 600; letter-spacing: 0.5px; }
    .content-list { padding-left: 15px; color: #E0E0E0; font-size: 0.95em; line-height: 1.5; margin: 0; }
    .content-list li { margin-bottom: 6px; }
    .insight-label { color: #aaa; font-weight: 500; }
    .insight-val { color: #fff; font-weight: 600; }
    .glance-box { background-color:#252A33; padding:10px; border-radius:6px; text-align:center; border:1px solid #333; }
    .glance-label { font-size:0.75em; color:#888; text-transform:uppercase; }
    .glance-val { font-size:0.95em; color:#fff; font-weight:bold; margin-top:2px; }
    </style>
    """, unsafe_allow_html=True)
    
    risk_class = "risk-badge-low" if "Low" in comp['risk'] else "risk-badge-med" if "Medium" in comp['risk'] else "risk-badge-high"
    snap = comp.get('snapshot', {})
    
    # helper to render list
    def render_list_items(items):
        if isinstance(items, list):
            return ''.join([f'<li>{i}</li>' for i in items])
        return f'<li>{items}</li>'

    # --- AT A GLANCE BAR ---
    st.markdown(f"""
<div class="company-card">
  <div style="display:flex; justify-content:space-between; align-items:start; margin-bottom: 15px;">
    <div>
      <h1 style="margin:0; color:#4DA6FF; font-size: 2.2em;">{comp['name']}</h1>
      <div style="font-size:1.1em; color:#aaa; margin-top:4px;">{comp['ticker']} | {comp['sector']}</div>
    </div>
    <span class="{risk_class}" style="font-size: 1em;">{comp['risk']} Risk</span>
  </div>

  <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:10px; margin-bottom:25px;">
     <div class="glance-box"><div class="glance-label">Position</div><div class="glance-val">{snap.get('market_position','N/A')}</div></div>
     <div class="glance-box"><div class="glance-label">Horizon</div><div class="glance-val">{snap.get('horizon','N/A')}</div></div>
     <div class="glance-box"><div class="glance-label">Volatility</div><div class="glance-val">{snap.get('volatility','N/A')}</div></div>
     <div class="glance-box"><div class="glance-label">Style</div><div class="glance-val" style="color:#00CC96;">{snap.get('style','N/A')}</div></div>
  </div>
""", unsafe_allow_html=True)

    # --- GROWTH CHART (CONCEPTUAL) ---
    st.markdown('<div class="sub-head">📈 Conceptual Growth Trajectory (Past -> Future)</div>', unsafe_allow_html=True)
    
    # Generate synthetic chart data using standard python (No heavy pandas/numpy)
    import math
    import random
    
    archetype = comp.get('growth_archetype', 'Steady')
    points = 50
    data_values = []
    
    for i in range(points):
        x = i / 5.0 # 0 to 10 scale
        if archetype == 'Compounder':
            # Steady Exponential
            val = 100 * (1.15 ** x) + random.uniform(-2, 2)
        elif archetype == 'Cyclical':
            # Sine wave + trend
            val = 100 + (10 * x) + (20 * math.sin(x))
        elif archetype == 'Defensive':
            # Slow steady
            val = 100 * (1.08 ** x)
        elif archetype == 'FastGrowth':
            # High growth
            val = 100 * (1.25 ** x) + random.uniform(-5, 5)
        else: # Turnaround/Volatile
            val = 100 + (5 * x) + random.uniform(-15, 15)
        data_values.append(val)
        
    st.line_chart(data_values, height=200, use_container_width=True)
    st.caption("Note: Chart is completely conceptual to visualize the *nature* of growth, not actual price data.")



    # --- HELPER: INSIGHT TILES ---
    def render_kv_tile(label, val, indicator=None):
        val_color = "#4caf50" if "High" in val or "Strong" in val else "#ff5252" if "Low" in val or "Weak" in val else "#fff"
        return f"""
        <div style="background:#2A2F38; padding:10px; border-radius:6px; margin-bottom:8px; border-left:2px solid #555;">
            <div style="font-size:0.75em; color:#aaa; text-transform:uppercase;">{label}</div>
            <div style="font-size:0.95em; color:{val_color}; font-weight:600;">{val}</div>
        </div>
        """

    def render_risk_chip(r):
        color = "#3d0f0f" if "High" in r['level'] else "#3d3d0f" if "Med" in r['level'] else "#1E232B"
        text_color = "#ff5252" if "High" in r['level'] else "#ffeb3b"
        return f'<span style="background:{color}; color:{text_color}; padding:4px 8px; border-radius:4px; font-size:0.8em; margin-right:5px; border:1px solid {text_color}; display:inline-block; margin-bottom:5px;">{r["name"]}</span>'

    # --- TILE GRID LAYOUT ---
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown('<div class="section-head">🏢 Business Model</div>', unsafe_allow_html=True)
        bus = comp.get('dash_business', {})
        st.markdown(render_kv_tile("Revenue Source", bus.get('Source', 'N/A')), unsafe_allow_html=True)
        st.markdown(render_kv_tile("Customer Base", bus.get('Customer', 'N/A')), unsafe_allow_html=True)
        st.markdown(render_kv_tile("Scalability", bus.get('Scalability', 'N/A')), unsafe_allow_html=True)

        st.markdown('<div class="section-head">⚡ Risk Radar</div>', unsafe_allow_html=True)
        risks = comp.get('dash_risks', [])
        st.markdown("".join([render_risk_chip(r) for r in risks]), unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="section-head">🌍 Industry Context</div>', unsafe_allow_html=True)
        ind = comp.get('dash_industry', {})
        st.markdown(render_kv_tile("Sector Growth", ind.get('Growth', 'N/A')), unsafe_allow_html=True)
        st.markdown(render_kv_tile("Competition", ind.get('Competition', 'N/A')), unsafe_allow_html=True)
        st.markdown(render_kv_tile("Cyclicality", ind.get('Cyclicality', 'N/A')), unsafe_allow_html=True)

        st.markdown('<div class="section-head">🏰 Moat</div>', unsafe_allow_html=True)
        for m in comp.get('dash_moat', []):
            st.markdown(f'<span style="background:#0f3d0f; color:#4caf50; padding:2px 8px; border-radius:12px; font-size:0.8em; margin-right:4px; border:1px solid #4caf50;">{m}</span>', unsafe_allow_html=True)


    with c3:
        st.markdown('<div class="section-head">💵 Financial Health</div>', unsafe_allow_html=True)
        fin = comp.get('dash_financials', {})
        st.markdown(render_kv_tile("Revenue Trend", fin.get('Rev Trend', 'N/A')), unsafe_allow_html=True)
        st.markdown(render_kv_tile("Profitability", fin.get('Profit Stability', 'N/A')), unsafe_allow_html=True)
        st.markdown(render_kv_tile("Debt Comfort", fin.get('Debt Comfort', 'N/A')), unsafe_allow_html=True)

        st.markdown('<div class="section-head">🔮 Outlook</div>', unsafe_allow_html=True)
        out = comp.get('dash_outlook', {})
        st.markdown(render_kv_tile("Primary Driver", out.get('Driver', 'N/A')), unsafe_allow_html=True)
        st.markdown(render_kv_tile("Mgmt Quality", out.get('Management', 'N/A')), unsafe_allow_html=True)


    # --- CHECKLIST TABLE ---
    checklist_rows = ""
    if 'checklist_expanded' in comp:
        for item in comp['checklist_expanded']:
            status_color = "#4caf50" if item['status'] in ['Yes', 'Strong', 'Wide'] else "#ffeb3b" if "Moderate" in item['status'] else "#ff5252"
            checklist_rows += f'<div class="checklist-row"><span style="color:#ccc;">{item["item"]}</span><span style="color:{status_color}; font-weight:bold;">{item["status"]}</span><span style="color:#888; font-size:0.9em;">{item["detail"]}</span></div>'

    st.markdown(f"""
  <!-- SUITABILITY -->
  <div style="background-color: #252A33; padding: 15px; border-radius: 8px; margin-top: 25px; border-left: 4px solid #00CC96;">
      <div style="font-size: 0.85em; color: #00CC96; font-weight:bold; letter-spacing:1px; margin-bottom:5px;">INVESTOR SUITABILITY</div>
      <div style="font-size: 1.05em; color: #fff;">{comp.get('suitability_detailed', comp['suitability'])}</div>
  </div>

  <!-- CHECKLIST -->
  <div style="background-color: #262B33; padding: 20px; border-radius: 12px; margin-top: 25px; border: 1px solid #444;">
    <div class="section-head" style="margin-top:0; border:none; padding-left:0;">✅ Decision Checklist</div>
    <div style="margin-top:10px;">{checklist_rows}</div>
  </div>

  <!-- DISCLAIMER -->
  <div style="background-color: #332b00; padding: 15px; border-radius: 8px; margin-top: 25px; font-size: 0.8em; color: #ffeb3b; text-align: center; border: 1px solid #ffcc00; line-height: 1.4;">
    <strong>⚠️ DISCLAIMER:</strong> This analysis is for <strong>educational and academic purposes only</strong>. 
    It does not constitute investment advice, stock recommendations, or solicitation. 
    Market investments are subject to risk. Past performance is not indicative of future results.
    Ref: SEBI/NISM Educational Standards.
  </div>
</div>
""", unsafe_allow_html=True)

