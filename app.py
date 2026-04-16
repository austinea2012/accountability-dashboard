import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ------------------------------
# Page config
st.set_page_config(page_title="XYZ County Accountability Dashboard", layout="wide")

# ========== BRANDING ==========
# Set the correct path to your logo file
# Replace "musewe-analytics-logo.png" with your actual file name
logo_path = Path(__file__).parent / "musewe-analytics-logo.png"

if logo_path.exists():
    st.sidebar.image(str(logo_path), width=150)
else:
    st.sidebar.warning("Logo file not found. Please check the file name and path.")
st.sidebar.markdown("## Musewe Analytics")
st.sidebar.markdown("---")
# ===============================

st.title("🏛️ XYZ County Accountability Dashboard")
st.markdown("**Linking the County Manifesto → CIDP → Programme Budget**")
st.markdown("Track pledges, budgets, and performance. *Actuals (spending & physical progress) will be added soon.*")
st.markdown("---")

# ------------------------------
# 1. Key Financial Metrics (example data – replace with your county's figures)
total_budget = 12_793_339_678  # Ksh
recurrent = 6_974_551_487
development = 5_818_788_191
equitable_share = 7_754_478_885
osr = 3_114_920_823

# 2. Sector-wise budget (example – replace with your county's data)
sector_budget = pd.DataFrame({
    "Sector": [
        "County Assembly", "Governance & Admin", "Finance & Planning",
        "Agriculture", "Water & Environment", "Education & Social Services",
        "Health", "Lands & Housing", "Roads & Public Works",
        "Trade & Industrialization", "Tourism & Sports"
    ],
    "Recurrent (Ksh M)": [779.9, 362.7, 1406.3, 295.9, 93.9, 387.0, 2591.5, 137.1, 121.3, 265.6, 146.9],
    "Development (Ksh M)": [581.3, 80.1, 70.0, 578.1, 465.7, 620.6, 775.4, 124.1, 1706.9, 395.3, 167.2]
})
sector_budget["Total (Ksh M)"] = sector_budget["Recurrent (Ksh M)"] + sector_budget["Development (Ksh M)"]

# 3. Manifesto Pledges (example – replace with your county's pledges)
pledges = pd.DataFrame({
    "Pledge": [
        "Upgrade referral hospital",
        "Construct affordable housing units",
        "Increase water access to 65%",
        "Drill & equip boreholes",
        "Construct ECD centres",
        "Implement school feeding programme",
        "Complete county stadium",
        "Upgrade roads to bitumen standards",
        "Establish industrial park",
        "Revive cash crop farming"
    ],
    "Sector": [
        "Health", "Lands & Housing", "Water", "Water",
        "Education", "Education", "Sports", "Roads",
        "Trade", "Agriculture"
    ],
    "CIDP Reference": [
        "Hospital complex", "Housing units", "Water access target",
        "Boreholes", "New ECD centres", "Feeding programme",
        "Stadium", "Bitumen roads", "Industrial park", "Value chain"
    ],
    "Budget 2025/26 (Ksh M)": [93.6, 50.0, 465.7, 35.0, 351.6, 77.0, 19.5, 1706.9, 6.0, 15.0],
    "Target (CIDP)": [
        "1 complex", "24 units", "65% coverage", "100 boreholes",
        "30 centres", "50,000 learners", "1 stadium", "23 km",
        "1 park", "Revived"
    ],
    "Status (Planned)": ["Budgeted"] * 10
})

# 4. Sample sector projects (example)
projects = pd.DataFrame({
    "Project": [
        "Drilling & equipping borehole A", "Water pipeline extension B",
        "Construction of ECD centre C", "Market construction D"
    ],
    "Ward": ["Ward 1", "Ward 2", "Ward 3", "Ward 4"],
    "Budget (Ksh M)": [3.5, 2.0, 4.5, 6.0],
    "Status": ["Planned", "Planned", "Planned", "Planned"]
})

# 5. Performance indicators (example – replace with your county's KPIs)
indicators = pd.DataFrame({
    "Indicator": [
        "Immunization coverage (%)", "Contraceptive use (%)",
        "Skilled birth attendance (%)", "HIV prevalence (%)",
        "Malaria prevalence (%)"
    ],
    "Baseline (2022)": [98.4, 39.6, 98, 14.7, 19],
    "Target (2027)": [100, 50, 96, 10, 15],
    "Current (placeholder)": [98.5, 41, 98, 14.5, 18]
})

# 6. Revenue projections (example)
revenue = pd.DataFrame({
    "Year": ["2025/26", "2026/27", "2027/28"],
    "Equitable Share (Ksh B)": [7.75, 8.53, 9.38],
    "Own Source Revenue (Ksh B)": [3.11, 3.73, 3.90],
    "Conditional Grants (Ksh B)": [0.96, 0.91, 0.91]
})

# ------------------------------
# Sidebar Filters
st.sidebar.header("🔍 Filters")
selected_sector = st.sidebar.multiselect(
    "Select Sector", options=sector_budget["Sector"].unique(),
    default=sector_budget["Sector"].unique()
)
selected_pledge_sector = st.sidebar.multiselect(
    "Filter Pledges by Sector", options=pledges["Sector"].unique(),
    default=pledges["Sector"].unique()
)

# ------------------------------
# Dashboard Layout

# Row 1: Key Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Budget 2025/26", f"KES {total_budget/1e9:.2f} B")
with col2:
    st.metric("Recurrent Expenditure", f"KES {recurrent/1e9:.2f} B", delta="54.5% of total")
with col3:
    st.metric("Development Expenditure", f"KES {development/1e9:.2f} B", delta="45.5% of total")
with col4:
    st.metric("Own Source Revenue Target", f"KES {osr/1e6:.0f} M", delta="↑ from 2024/25")

st.markdown("---")

# Row 2: Sector Budget Breakdown
st.subheader("📊 Sector Budget Allocation (2025/26)")
filtered_sector = sector_budget[sector_budget["Sector"].isin(selected_sector)]
fig_sector = px.bar(
    filtered_sector, x="Sector", y=["Recurrent (Ksh M)", "Development (Ksh M)"],
    title="Recurrent vs Development by Sector",
    barmode="group", text_auto=True
)
st.plotly_chart(fig_sector, use_container_width=True)

# Row 3: Revenue Trends
st.subheader("💰 Revenue Projections (2025-2028)")
fig_rev = px.line(
    revenue, x="Year", y=["Equitable Share (Ksh B)", "Own Source Revenue (Ksh B)", "Conditional Grants (Ksh B)"],
    markers=True, title="Revenue Sources"
)
st.plotly_chart(fig_rev, use_container_width=True)

# Row 4: Pledge Tracker
st.subheader("📜 Manifesto Pledge Tracker (Budget & CIDP Alignment)")
filtered_pledges = pledges[pledges["Sector"].isin(selected_pledge_sector)]
st.dataframe(
    filtered_pledges[["Pledge", "Sector", "Budget 2025/26 (Ksh M)", "Target (CIDP)", "Status (Planned)"]],
    use_container_width=True, hide_index=True
)

# Row 5: Performance Indicators (Placeholder for actuals)
st.subheader("📈 Key Performance Indicators (Baseline vs Target)")
fig_ind = go.Figure()
fig_ind.add_trace(go.Bar(x=indicators["Indicator"], y=indicators["Baseline (2022)"],
                         name="Baseline 2022", marker_color="lightblue"))
fig_ind.add_trace(go.Bar(x=indicators["Indicator"], y=indicators["Target (2027)"],
                         name="Target 2027", marker_color="darkblue"))
fig_ind.add_trace(go.Bar(x=indicators["Indicator"], y=indicators["Current (placeholder)"],
                         name="Current (placeholder)", marker_color="orange"))
fig_ind.update_layout(title="Performance Indicators (Actuals to be updated)", barmode="group")
st.plotly_chart(fig_ind, use_container_width=True)

# Row 6: Sample Projects
st.subheader("🏗️ Sample Projects (2025/26 Budget)")
st.dataframe(projects, use_container_width=True, hide_index=True)

# Row 7: Future Actuals Placeholder
st.markdown("---")
st.subheader("📈 Coming Soon: Actual Expenditure & Physical Progress")
st.info("""
Once quarterly expenditure reports and project completion data are available, this dashboard will display:
- Actual spending vs budget (variance analysis)
- Physical targets achieved (e.g., km of roads done, boreholes completed)
- Real-time traffic lights for each pledge
- Ward-level performance maps
""")

# Row 8: Data Download
st.subheader("📥 Export Data")
csv_pledges = filtered_pledges.to_csv(index=False).encode('utf-8')
st.download_button("Download Pledge Tracker (CSV)", csv_pledges, "xyz_pledges.csv", "text/csv")

# Footer
st.markdown("---")
st.caption("Data sources: County Manifesto, CIDP, Programme Based Budget. Actuals will be added from IFMIS and departmental reports.")
