import streamlit as st
import pandas as pd
import requests

from utils.api import API_URL

API_BASE = f"{API_URL}/api"

def display_policy_dashboard():
    # 1️⃣ Dashboard Header
    st.title("📊 Policy Insights Dashboard")
    st.markdown("Real-time economic impact monitoring & citizen welfare tracking.")
    
    try:
        res = requests.get(f"{API_BASE}/data/users-insights")
        if res.status_code == 200:
            data = res.json()
            
            # --- HELPER: EMPTY STATE RENDERER ---
            def render_empty_dashboard_state():
                st.markdown("""
                <div style="text-align: center; padding: 40px; background-color: #161B22; border-radius: 12px; border: 1px solid #30363D; margin-bottom: 30px;">
                    <div style="font-size: 3rem; margin-bottom: 10px;">📊</div>
                    <h2 style="color: #8B949E; margin: 0;">Policy Monitoring Status</h2>
                    <p style="font-size: 1.1rem; color: #FAFAFA; margin-top: 10px;">No household financial simulations have been submitted yet.</p>
                    <p style="color: #8B949E;">Policy insights will appear automatically once citizen data is available.</p>
                </div>
                """, unsafe_allow_html=True)
                
                c_status, c_preview = st.columns(2)
                
                with c_status:
                    st.subheader("🔍 Data Availability Check")
                    with st.container(border=True):
                        st.markdown("""
                        - **Registered Households:** ✅ System Active
                        - **Financial Simulations:** ❌ None Submitted
                        - **Policy Insights:** ⏳ Pending Data
                        """)
                        st.caption("System is online and waiting for user inputs.")

                with c_preview:
                    st.subheader("🔮 What Will Appear Here")
                    st.info("""
                    **Future Insights:**
                    - 🏠 Income vs Inflation Stress Map
                    - 📉 Most Affected Expense Categories
                    - ⚠️ Identification of At-Risk Groups
                    - 💡 Data-driven Policy Recommendations
                    """)

                st.markdown("### 🚀 Next Steps for Policy Makers")
                with st.container(border=True):
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.markdown("**1. Monitor Registrations**")
                        st.caption("Ensure citizens are signing up.")
                    with c2:
                        st.markdown("**2. Encourage Participation**")
                        st.caption("Ask users to run the inflation calculator.")
                    with c3:
                        st.markdown("**3. Contact Citizens**")
                        st.caption("Use the 'Contact Users' tab to reach out.")
            
            if not data:
                render_empty_dashboard_state()
                return

            # --- PRE-PROCESSING ---
            insights = []
            for item in data:
                fin = item.get('financials')
                if not fin:
                    continue
                    
                # Calculate metrics for display
                salary = float(fin.get('salary', 0))
                current_spend = float(fin.get('total_spend', 0))
                future_spend = float(fin.get('future_total_spend', 0))
                impact = future_spend - current_spend
                
                # Determine Severity (Display Logic)
                if future_spend > salary:
                    status = "Critical"
                    severity_score = 3
                elif future_spend > (salary * 0.9):
                    status = "Watchlist"
                    severity_score = 2
                else:
                    status = "Stable"
                    severity_score = 1
                    
                insights.append({
                    "Name": item.get('username', 'Unknown'),
                    "Phone": item.get('phone', 'N/A'),
                    "Group": item.get('household_group', 'Unclassified'),
                    "Monthly Income": salary,
                    "Inflation Impact": impact,
                    "Future Spend": future_spend,
                    "Status": status,
                    "Most Affected": fin.get('most_affected_category', 'None'),
                    "_severity": severity_score # Hidden helper
                })

            df = pd.DataFrame(insights)
            if df.empty:
                render_empty_dashboard_state()
                return

            # --- 1️⃣ EXECUTIVE SUMMARY (KPI Cards) ---
            total_h = len(df)
            critical_h = len(df[df['Status'] == 'Critical'])
            stable_h = len(df[df['Status'] == 'Stable'])
            
            # Most affected cat
            if not df['Most Affected'].empty:
                top_issue = df['Most Affected'].mode()[0]
                affected_pct = int((len(df[df['Most Affected'] == top_issue]) / total_h) * 100)
            else:
                top_issue = "None"
                affected_pct = 0

            st.markdown("### 📢 Executive Summary")
            k1, k2, k3, k4 = st.columns(4)
            
            with k1:
                st.metric("Households Tracked", total_h, "Active")
            with k2:
                st.metric("Critical Distress", critical_h, f"{int(critical_h/total_h*100)}% of Total", delta_color="inverse")
            with k3:
                st.metric("Financially Stable", stable_h, "Low Risk")
            with k4:
                st.metric("Top Issue", top_issue, f"Impacts {affected_pct}%")

            st.divider()

            # --- 2️⃣ ADVANCED HOUSEHOLD IMPACT TABLE ---
            st.subheader("📋 Policy Analysis Table")
            
            # Severity Logic Explanation
            with st.expander("ℹ️ How Severity is Calculated", expanded=False):
                st.caption("Severity is based on Income vs. Inflation-Adjusted Spending Projections.")
                st.caption("🔴 Critical: Projected cost exceeds income.")
                st.caption("🟡 Watchlist: Projected cost is >90% of income.")
                st.caption("🟢 Stable: Income comfortably covers costs.")
            
            # Formatting with Column Config
            st.dataframe(
                df.drop(columns=['_severity']),
                column_config={
                    "Monthly Income": st.column_config.NumberColumn(format="₹%d"),
                    "Inflation Impact": st.column_config.NumberColumn(format="₹%d", help="Projected cost increase"),
                    "Future Spend": st.column_config.NumberColumn(format="₹%d"),
                    "Status": st.column_config.TextColumn(
                        "Risk Status",
                        help="Financial stability",
                        validate=None
                    ),
                    "Most Affected": "Top Expense"
                },
                use_container_width=True,
                hide_index=True
            )
            
            st.divider()
            
            # --- 3️⃣ GROUP-WISE IMPACT ANALYSIS ---
            st.subheader("🏙️ Group-Wise Impact Analysis")
            
            # Group by and aggregation
            grp_df = df.groupby("Group").agg({
                "Monthly Income": "mean",
                "Inflation Impact": "mean",
                "_severity": "mean"
            }).reset_index()
            
            grp_df["Avg Risk Level"] = grp_df["_severity"].apply(lambda x: "High" if x > 2.5 else "Medium" if x > 1.5 else "Low")
            
            # Display visually
            c_grp = st.columns(3)
            for idx, row in grp_df.iterrows():
                with c_grp[idx % 3]:
                    st.markdown(f"""
                    <div style="background-color: #21262D; border: 1px solid #30363D; border-radius: 8px; padding: 15px; margin-bottom: 10px;">
                        <div style="font-weight: bold; color: #4DA6FF; margin-bottom: 5px;">{row['Group']}</div>
                        <div style="font-size: 0.9rem; color: #8B949E;">Avg Impact: <span style="color: #FAFAFA;">₹{int(row['Inflation Impact'])}</span></div>
                        <div style="font-size: 0.9rem; color: #8B949E;">Avg Income: <span style="color: #FAFAFA;">₹{int(row['Monthly Income'])}</span></div>
                        <div style="margin-top: 8px; font-size: 0.8rem; background: #30363D; display: inline-block; padding: 2px 8px; border-radius: 4px;">
                            Risk: {row['Avg Risk Level']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            # --- 4️⃣ POLICY RECOMMENDATIONS & OUTREACH ---
            st.divider()
            r_col, a_col = st.columns([1.5, 1])
            
            with r_col:
                st.subheader("💡 Policy Recommendations")
                st.markdown(f"""
                <div style="background-color: #1F242C; padding: 15px; border-radius: 8px; border-left: 4px solid #00CC96;">
                    <strong>Observation:</strong> {top_issue} is the leading driver of household stress.<br>
                    <strong>Suggestion:</strong> Consider subsidies or supply chain interventions for {top_issue} in {grp_df.loc[grp_df['Inflation Impact'].idxmax()]['Group']} areas.
                </div>
                <div style="margin-top: 10px; background-color: #1F242C; padding: 15px; border-radius: 8px; border-left: 4px solid #E1AD01;">
                    <strong>Observation:</strong> {critical_h} households are in Critical financial territory.<br>
                    <strong>Suggestion:</strong> Activate direct benefit transfer (DBT) review for high-risk families.
                </div>
                """, unsafe_allow_html=True)
                
            with a_col:
                st.subheader("📢 Outreach Actions")
                st.caption("Take immediate action on filtered data.")
                
                with st.expander("✉️ Contact High-Risk Households"):
                    st.dataframe(df[df['Status'] == 'Critical'][['Name', 'Phone']], hide_index=True)
                
                c1, c2 = st.columns(2)
                c1.button("🚩 Flag for Review", use_container_width=True)
                c2.button("📥 Export Report", use_container_width=True)

        else:
            st.error("Failed to fetch insight data.")
    except Exception as e:
        st.error(f"System Error: {e}")

def display_contact_users():
    st.header("Contact Citizens")
    try:
        res = requests.get(f"{API_BASE}/data/users-insights")
        if res.status_code == 200:
            data = res.json()
            for user in data:
                grp = user.get('household_group', 'Unknown')
                fin = user.get('financials')
                affected = fin['most_affected_category'] if fin else "Unknown"
                
                with st.expander(f"👤 {user['username']} ({grp}) - {affected}"):
                    st.write(f"**Most Affected By:** {affected}")
                    st.write(f"**Phone:** {user['phone']}")
                    st.write(f"**Address:** {user.get('address', 'Not Provided')}")
                    st.markdown(f"[📞 Call Now](tel:{user['phone']})")
    except Exception as e:
        st.error(f"Error: {e}")
