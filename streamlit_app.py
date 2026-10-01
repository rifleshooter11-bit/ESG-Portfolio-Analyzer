import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ESG Portfolio Analyzer",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS STYLING FOR PROFESSIONAL LIGHT THEME ---
st.markdown("""
    <style>
        .stApp {
            background-color: #f8f9fa;
        }
        .metric-card {
            background-color: #ffffff;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            border: 1px solid #e9ecef;
            text-align: center;
        }
        .metric-title {
            color: #6c757d;
            font-size: 14px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 10px;
        }
        .metric-value {
            color: #212529;
            font-size: 28px;
            font-weight: 700;
        }
        h1, h2, h3 {
            color: #1a1a1a;
            font-weight: 700;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    data_path = "esg_data.csv"
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    else:
        return pd.DataFrame()

df = load_data()

# --- SIDEBAR ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3233/3233483.png", width=60)
st.sidebar.title("ESG Analytics")
st.sidebar.markdown("---")

if not df.empty:
    st.sidebar.subheader("Filters")
    selected_sectors = st.sidebar.multiselect(
        "Select Sectors",
        options=df["Sector"].unique(),
        default=df["Sector"].unique()
    )
    
    # Filter dataset
    filtered_df = df[df["Sector"].isin(selected_sectors)]
    
    st.sidebar.markdown("---")
    st.sidebar.info("💡 **Note:** Lower ESG Risk Score indicates better ESG performance (lower risk).")

# --- MAIN DASHBOARD ---
st.title("🍃 Professional ESG Portfolio Dashboard")
st.markdown("Analyze environmental, social, and governance risk across your equity portfolio.")

if df.empty:
    st.warning("No data found! Please run `python fetch_esg_data.py` to generate the `esg_data.csv` dataset first.")
    st.stop()

# --- TOP METRICS ---
col1, col2, col3, col4 = st.columns(4)
avg_risk = filtered_df["Total ESG Risk Score"].mean()
total_mc = filtered_df["Market Cap ($B)"].sum()
best_company = filtered_df.loc[filtered_df["Total ESG Risk Score"].idxmin()]
worst_company = filtered_df.loc[filtered_df["Total ESG Risk Score"].idxmax()]

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Avg Portfolio ESG Risk</div>
        <div class="metric-value">{avg_risk:.1f}</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Portfolio Market Cap</div>
        <div class="metric-value">${total_mc:,.0f}B</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">ESG Leader</div>
        <div class="metric-value">{best_company['Ticker']} ({best_company['Total ESG Risk Score']})</div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Highest Risk</div>
        <div class="metric-value">{worst_company['Ticker']} ({worst_company['Total ESG Risk Score']})</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- CHARTS ROW 1 ---
st.subheader("Risk Distribution & Sector Analysis")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    # Scatter plot: Market Cap vs ESG Risk
    fig_scatter = px.scatter(
        filtered_df, 
        x="Total ESG Risk Score", 
        y="Market Cap ($B)", 
        size="Market Cap ($B)", 
        color="Sector",
        hover_name="Company Name",
        title="Market Cap vs. ESG Risk Score",
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    # Reverse X axis since lower risk is better
    fig_scatter.update_xaxes(autorange="reversed")
    st.plotly_chart(fig_scatter, use_container_width=True)

with chart_col2:
    # Box plot: ESG Risk by Sector
    fig_box = px.box(
        filtered_df, 
        x="Sector", 
        y="Total ESG Risk Score",
        color="Sector",
        title="ESG Risk Distribution by Sector",
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    st.plotly_chart(fig_box, use_container_width=True)

# --- CHARTS ROW 2 ---
st.subheader("Pillar Breakdown (E, S, G)")
chart_col3, chart_col4 = st.columns([2, 1])

with chart_col3:
    # Stacked bar chart for E, S, G components
    df_melted = filtered_df.melt(
        id_vars=["Ticker", "Sector"], 
        value_vars=["Environmental Risk", "Social Risk", "Governance Risk"],
        var_name="Pillar", 
        value_name="Score"
    )
    
    fig_bar = px.bar(
        df_melted, 
        x="Ticker", 
        y="Score", 
        color="Pillar",
        title="ESG Risk Breakdown by Company",
        template="plotly_white",
        color_discrete_map={
            "Environmental Risk": "#006b54", 
            "Social Risk": "#4e73df", 
            "Governance Risk": "#f6c23e"
        }
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with chart_col4:
    # Donut chart for ESG Ratings
    rating_counts = filtered_df["ESG Rating"].value_counts().reset_index()
    rating_counts.columns = ["Rating", "Count"]
    
    fig_pie = px.pie(
        rating_counts, 
        values="Count", 
        names="Rating", 
        hole=0.6,
        title="Portfolio ESG Ratings",
        template="plotly_white",
        color_discrete_sequence=px.colors.sequential.Teal
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# --- DATA TABLE ---
st.subheader("Detailed Company Data")
st.dataframe(
    filtered_df.style.format({
        "Market Cap ($B)": "{:,.2f}",
        "P/E Ratio": "{:.2f}",
        "Total ESG Risk Score": "{:.1f}",
        "Environmental Risk": "{:.1f}",
        "Social Risk": "{:.1f}",
        "Governance Risk": "{:.1f}"
    }).background_gradient(cmap="Greens_r", subset=["Total ESG Risk Score"]),
    use_container_width=True,
    height=300
)
