
import json
import pprint
import random

# Import existing data
from frontend.data.company_data import COMPANIES

# --- DASHBOARD INTELLIGENCE (EXECUTIVE ANALYST STYLE) ---

SECTOR_DASHBOARD = {
    "Banking": {
        "business": {"Source": "Net Interest Trend", "Customer": "Retail & Corporate", "Dependency": "Economy (High)", "Scalability": "High"},
        "industry": {"Growth": "12-15% (Credit)", "Competition": "Intense", "Regulation": "High (RBI)", "Cyclicality": "High"},
        "moat": ["Low Cost Funds", "Brand Trust", "Branch Network"],
        "financials": {"Rev Trend": "↑ Rising", "Profit Stability": "→ Stable", "Cash Flow": "✔ LCR > 110%", "Debt Comfort": "N/A (Bank)"},
        "risks": [{"name": "Asset Quality", "level": "Medium"}, {"name": "Regulatory", "level": "High"}, {"name": "Tech Disruption", "level": "Med"}],
        "outlook": {"Driver": "Credit Uptake", "Strategy": "Digital First", "Management": "✔ Professional"}
    },
    "IT Services": {
        "business": {"Source": "Export Services (USD)", "Customer": "Global Fortune 500", "Dependency": "US/EU Macro", "Scalability": "Very High"},
        "industry": {"Growth": "8-10% (Steady)", "Competition": "Global Oligopoly", "Regulation": "Low", "Cyclicality": "Moderate"},
        "moat": ["Client Switching Costs", "Talent Scale", "Deep Domain"],
        "financials": {"Rev Trend": "→ Steady", "Profit Stability": "✔ High", "Cash Flow": "✔ Robust FCF", "Debt Comfort": "✔ Zero Debt"},
        "risks": [{"name": "US Recession", "level": "High"}, {"name": "AI Disruption", "level": "High"}, {"name": "Currency", "level": "Med"}],
        "outlook": {"Driver": "Cloud & AI Transformation", "Strategy": "Large Deals", "Management": "✔ Best-in-Class"}
    },
    "FMCG": {
        "business": {"Source": "Volume x Price Mix", "Customer": "Mass Consumer", "Dependency": "Rural Demand", "Scalability": "High"},
        "industry": {"Growth": "GDP + 2%", "Competition": "Fragmented", "Regulation": "Moderate", "Cyclicality": "Low (Defensive)"},
        "moat": ["Mindshare (Brand)", "Distribution Reach", "Pricing Power"],
        "financials": {"Rev Trend": "→ Slow", "Profit Stability": "✔ Very High", "Cash Flow": "✔ Cash Cow", "Debt Comfort": "✔ Zero/Low"},
        "risks": [{"name": "Raw Material Infl.", "level": "Med"}, {"name": "Rural Slowdown", "level": "High"}, {"name": "Competition", "level": "Med"}],
        "outlook": {"Driver": "Premiumization", "Strategy": "Volume Recovery", "Management": "✔ MNC Standards"}
    },
    "Automobile": {
        "business": {"Source": "Vehicle Sales", "Customer": "Discretionary", "Dependency": "Eco Cycle", "Scalability": "Med (Capex)"},
        "industry": {"Growth": "Cyclical Upswing", "Competition": "High", "Regulation": "High (Emission)", "Cyclicality": "Very High"},
        "moat": ["Brand Aspirations", "Service Network", "Mfg Scale"],
        "financials": {"Rev Trend": "↑ Strong", "Profit Stability": "⚠ Volatile", "Cash Flow": "→ Improving", "Debt Comfort": "→ Manageable"},
        "risks": [{"name": "EV Transition", "level": "High"}, {"name": "Commodity Prices", "level": "High"}, {"name": "Demand Cycle", "level": "High"}],
        "outlook": {"Driver": "EV & SUVs", "Strategy": "Electrification", "Management": "✔ Experienced"}
    },
    "NBFC": {
        "business": {"Source": "High Yield Loans", "Customer": "Retail/SME", "Dependency": "Liquidity", "Scalability": "High"},
        "industry": {"Growth": "15%+ (Fast)", "Competition": "Banks/Fintech", "Regulation": "Tightening", "Cyclicality": "High"},
        "moat": ["Agility/Speed", "Data Underwriting", "Niche Reach"],
        "financials": {"Rev Trend": "↑ Rapid", "Profit Stability": "→ Good", "Cash Flow": "⚠ Negative (Growth)", "Debt Comfort": "→ High Leverage"},
        "risks": [{"name": "Funding Cost", "level": "High"}, {"name": "Unsecured Loans", "level": "High"}, {"name": "Regulatory", "level": "Med"}],
        "outlook": {"Driver": "Consumption", "Strategy": "Omnichannel", "Management": "✔ Aggressive"}
    },
    "Power": {
        "business": {"Source": "Power Gen (PPA)", "Customer": "Govt (Discoms)", "Dependency": "Policy", "Scalability": "Low (Asset Heavy)"},
        "industry": {"Growth": "GDP Linked", "Competition": "Low (Regulated)", "Regulation": "Very High", "Cyclicality": "Low"},
        "moat": ["Regulated Return", "Fuel Linkages", "Long Contracts"],
        "financials": {"Rev Trend": "→ Stable", "Profit Stability": "✔ Guaranteed", "Cash Flow": "→ Stable", "Debt Comfort": "⚠ High (Infra)"},
        "risks": [{"name": "Dues Recovery", "level": "High"}, {"name": "Green Transition", "level": "Med"}, {"name": "Fuel Supply", "level": "Med"}],
        "outlook": {"Driver": "Capacity Expansion", "Strategy": "Green Shift", "Management": "→ PSU/Stable"}
    }
}

def get_sector_dashboard(sector):
    for key in SECTOR_DASHBOARD:
        if key in sector:
            return SECTOR_DASHBOARD[key]
    
    # Fallback
    return {
        "business": {"Source": "Core Ops", "Customer": "Mixed", "Dependency": "Economy", "Scalability": "Moderate"},
        "industry": {"Growth": "GDP Linked", "Competition": "Moderate", "Regulation": "Moderate", "Cyclicality": "Moderate"},
        "moat": ["Market Position", "Operational Efficiency"],
        "financials": {"Rev Trend": "→ Stable", "Profit Stability": "→ Stable", "Cash Flow": "→ Positive", "Debt Comfort": "→ Manageable"},
        "risks": [{"name": "Market Risk", "level": "Med"}, {"name": "Execution", "level": "Med"}],
        "outlook": {"Driver": "Organic Growth", "Strategy": "Consolidation", "Management": "✔ Professional"}
    }

ENRICHED_COMPANIES = []

for c in COMPANIES:
    dash = get_sector_dashboard(c['sector'])
    new_c = c.copy()
    
    # 1. Snapshot Components (Kept from previous, refined)
    new_c['snapshot'] = {
        "market_position": "Leader" if "Low" in c['risk'] else "Challenger" if "Medium" in c['risk'] else "Niche",
        "horizon": "Long Term" if "Low" in c['risk'] else "Medium Term" if "Medium" in c['risk'] else "Speculative",
        "volatility": "Low Beta" if "Low" in c['risk'] else "Med Beta" if "Medium" in c['risk'] else "High Beta",
        "style": "Compounder" if "Low" in c['risk'] else "Cyclical/Growth" if "Medium" in c['risk'] else "High Growth"
    }
    
    # 2. Assign Structured Dashboard Data
    new_c['dash_business'] = dash['business']
    new_c['dash_industry'] = dash['industry']
    new_c['dash_moat'] = dash['moat']
    new_c['dash_financials'] = dash['financials']
    new_c['dash_risks'] = dash['risks']
    new_c['dash_outlook'] = dash['outlook']
    
    # 3. Growth Archetype (Kept)
    new_c['growth_archetype'] = "Compounder" if "Low" in c['risk'] else "FastGrowth" if "High" in c['risk'] else "Cyclical"

    # 4. Checklist (Table Data - Kept)
    new_c['checklist_expanded'] = [
        {"item": "Profitability", "status": "Yes" if "True" in str(c['checklist'].get('Profitable')) else "No", "detail": "Operating High"},
        {"item": "Solvency", "status": "Strong" if "Low" in c['risk'] else "Mod", "detail": "Comfortable D/E"},
        {"item": "Moat", "status": "Wide" if "Low" in c['risk'] else "Narrow", "detail": "Defensible"},
        {"item": "Model", "status": "Simple" if "Low" in c['risk'] else "Complex", "detail": "Easy to understand"},
        {"item": "Trend", "status": "Up" if "Low" in c['risk'] else "Mixed", "detail": "Sector tailwinds"}
    ]
    
    ENRICHED_COMPANIES.append(new_c)

# Write to file
with open("frontend/data/company_data.py", "w", encoding="utf-8") as f:
    f.write("# PROFESSIONAL ANALYST DASHBOARD DATASETS\n")
    f.write("COMPANIES = " + pprint.pformat(ENRICHED_COMPANIES, width=120, sort_dicts=False))
