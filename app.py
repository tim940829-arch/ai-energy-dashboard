import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime

# ==========================================
# 1. Page Configuration (Surveillance Console Style)
# ==========================================
st.set_page_config(page_title="AI-Energy Surveillance", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for the Hacker/Terminal look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    h1, h2, h3 { color: #58a6ff !important; font-family: 'Courier New', Courier, monospace; }
    .status-bar { padding: 10px; background: #21262d; border-radius: 5px; color: #8b949e; font-size: 0.8rem; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. Define Monitoring Targets (2026 Core Portfolio)
# ==========================================
sectors = {
    "AI & Computing": ['NVDA', 'MSFT', 'TSM', 'AMD', 'SMCI', 'AVGO', 'GOOGL', 'AMZN'],
    "Energy & Utilities": ['VST', 'CEG', 'NEE', 'DUK', 'SO', 'AEP', 'PEG'],
    "Grid & Hardware": ['GEV', 'ETN', 'SU', 'VRT']
}
all_tickers = [ticker for sublist in sectors.values() for ticker in sublist]

# ==========================================
# 3. Data Fetching Module
# ==========================================
@st.cache_data(ttl=3600)
def fetch_financial_data(tickers, period):
    # Using 'Close' to ensure data consistency
    raw_data = yf.download(tickers, period=period)['Close']
    return raw_data

# ==========================================
# 4. Main Interface Layout
# ==========================================
st.title("🛡️ 2026 US Market AI-Energy Smart Surveillance")
st.markdown(f"<div class='status-bar'>SYSTEM STATUS: ACTIVE | DATABASE: YAHOO FINANCE | LAST UPDATED: {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>", unsafe_allow_html=True)
st.write("")

# Sidebar Parameters
with st.expander("📡 Surveillance Parameters"):
    period = st.select_slider("Observation Timeframe", options=['1mo', '3mo', '6mo', '1y', '2y', '5y'], value='1y')
    analysis_type = st.radio("Data Processing Mode", ["Correlation Matrix", "Cumulative Returns", "Volatility Distribution"], horizontal=True)

df = fetch_financial_data(all_tickers, period)

# Calculate Indicators
corr_matrix = df.corr()
returns = (df / df.iloc[0]) * 100

# ==========================================
# 5. Multi-Monitor Rendering
# ==========================================

# Row 1: Key Metrics Monitoring
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("AI Leader (NVDA)", f"${df['NVDA'].iloc[-1]:.2f}", f"{((df['NVDA'].iloc[-1]/df['NVDA'].iloc[-2])-1)*100:.2f}%")
with m2:
    st.metric("Utility Benchmark (VST)", f"${df['VST'].iloc[-1]:.2f}", f"{((df['VST'].iloc[-1]/df['VST'].iloc[-2])-1)*100:.2f}%")
with m3:
    # Find the non-tech stock with the highest correlation to NVDA
    high_corr_energy = corr_matrix.loc['NVDA', sectors["Energy & Utilities"]].idxmax()
    st.metric("Highest Correlated Energy", high_corr_energy, f"{corr_matrix.loc['NVDA', high_corr_energy]:.2f} Corr")
with m4:
    st.metric("Total Monitored Assets", len(all_tickers), "LIVE SCANNING")

st.write("")

# Row 2: Main Monitors
c1, c2 = st.columns([1.2, 0.8])

with c1:
    st.subheader("🖥️ MONITOR 01: Cross-Sector Correlation Heatmap")
    fig_heatmap = px.imshow(
        corr_matrix,
        labels=dict(color="Correlation"),
        x=corr_matrix.columns,
        y=corr_matrix.index,
        color_continuous_scale='Viridis',
        aspect="auto"
    )
    fig_heatmap.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="#58a6ff",
        margin=dict(l=0, r=0, t=30, b=0)
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

with c2:
    st.subheader("🖥️ MONITOR 02: Sector Return Trends")
    selected_sector = st.selectbox("Toggle Observation Sector", list(sectors.keys()))
    sector_returns = returns[sectors[selected_sector]]
    
    fig_line = px.line(
        sector_returns,
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    fig_line.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_line, use_container_width=True)

# Row 3: Deep Analysis
st.subheader("🔍 MONITOR 03: Smart Insights & Correlation Strength")
i1, i2 = st.columns(2)

with i1:
    # Scatter plot with OLS trendline for NVDA vs VST
    fig_scatter = px.scatter(
        df, x='NVDA', y='VST', 
        trendline="ols", 
        title="NVDA vs. VST Energy Resonance Analysis",
        template="plotly_dark"
    )
    fig_scatter.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="#58a6ff"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with i2:
    st.write("📋 **Current Market Scan Report**")
    latest_corr = corr_matrix['NVDA'].sort_values(ascending=False).head(6)
    st.dataframe(latest_corr, use_container_width=True)
    st.warning("⚠️ ALERT: If correlation exceeds 0.85, utility stocks are functioning as tech derivatives. Monitor energy policy risks closely.")