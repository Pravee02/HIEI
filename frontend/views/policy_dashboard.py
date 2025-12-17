import streamlit as st
import pandas as pd
import requests

API_BASE = "http://127.0.0.1:5000/api"

def display_policy_dashboard():
    st.header("Policy Insights Dashboard")
    st.markdown("Real-time data from registered households.")
    
    try:
        res = requests.get(f"{API_BASE}/data/users-insights")
        if res.status_code == 200:
            data = res.json()
            if data:
                # NEW LOGIC START
                insights = data 
                df = pd.DataFrame(insights)
                
                # Process Financials
                expenses = []
                for _, row in df.iterrows():
                    fin = row['financials']
                    if fin:
                        expenses.append({
                            "Name": row['username'],
                            "Phone": row['phone'],
                            "Group": row['household_group'],
                            "Salary": f"₹{int(fin['salary'])}",
                            "Total Impact": f"₹{int(fin['future_total_spend'] - fin['total_spend'])}", # Extra Cost due to inflation often
                            # Actually Total Impact roughly means Extra Cost prediction or just total spend? 
                            # Let's use Future - Current as Impact.
                            "Future Spend": f"₹{int(fin['future_total_spend'])}",
                            "Status": fin['salary_status'],
                            "Most Affected": fin['most_affected_category']
                        })
                    else:
                        expenses.append({
                            "Name": row['username'],
                            "Phone": row['phone'],
                            "Group": row['household_group'],
                            "Salary": "N/A",
                            "Total Impact": "N/A",
                            "Future Spend": "N/A",
                            "Status": "No Data",
                            "Most Affected": "N/A"
                        })
                        
                df_display = pd.DataFrame(expenses)
                
                # --- FILTERS ---
                st.sidebar.header("Filter Data")
                # Handle case where Group might be null/None in data
                unique_groups = [g for g in df_display['Group'].unique() if g]
                group_filter = st.sidebar.multiselect("Household Group", unique_groups, default=unique_groups)
                
                if not group_filter:
                    st.warning("Select a group to view data.")
                    # Fallthrough to show contact info? No, just return.
                    
                else:
                    filtered_df = df_display[df_display['Group'].isin(group_filter)]

                    # --- METRICS ---
                    total_tracked = len(filtered_df)
                    deficits = len(filtered_df[filtered_df['Status'] == "DEFICIT"])
                    surplus = len(filtered_df[filtered_df['Status'] == "SURPLUS"])
                    
                    try:
                        valid_affected = filtered_df[~filtered_df['Most Affected'].isin(["N/A", "Stable"])]
                        if not valid_affected.empty:
                            common_issue = valid_affected['Most Affected'].mode()[0]
                        else:
                            common_issue = "None"
                    except:
                        common_issue = "None"

                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Households Tracked", total_tracked)
                    m2.metric("In Deficit", deficits, delta_color="inverse")
                    m3.metric("Safe / Surplus", surplus)
                    m4.metric("Dominant Issue", common_issue)

                    st.divider()

                    # --- MAIN TABLE ---
                    st.subheader("Household Financial Impact Analysis")
                    
                    def highlight_status(val):
                        color = 'red' if val == 'DEFICIT' else 'green' if val == 'SURPLUS' else 'gray'
                        return f'color: {color}; font-weight: bold'

                    st.dataframe(
                        filtered_df.style.applymap(highlight_status, subset=['Status']),
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # --- ACTION SECTION ---
                    st.divider()
                    st.subheader("📢 Outreach & Policy Action")
                    
                    if deficits > 0:
                        st.error(f"🚨 ACTION REQUIRED: {deficits} Households are in financial deficit.")
                        with st.expander("View High Risk Households (Contact List)"):
                            risk_df = filtered_df[filtered_df['Status'] == "DEFICIT"][['Name', 'Phone', 'Group', 'Most Affected']]
                            st.table(risk_df)
                    else:
                        st.success("All tracked households are currently financially stable.")

            else:
                st.info("No registered users found in the system.")
        else:
            st.error("Failed to fetch insights from server.")
    except Exception as e:
        st.error(f"Connection Error: {e}")

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
