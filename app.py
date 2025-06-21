
import streamlit as st
import pandas as pd
from footprint_utils import plot_footprint, plot_volume_profile
from strategy import run_backtest
import datetime

st.set_page_config(layout="wide", page_title="Full MSI Strategy App")
st.title("📈 MSI Strategy Intelligence Dashboard")

uploaded_file = st.sidebar.file_uploader("📂 Upload Your Footprint Data", type=["csv", "xlsx"])
save_signals = st.sidebar.checkbox("✅ Save MSI Signals", value=True)

if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith("csv") else pd.read_excel(uploaded_file)

    # MSI Calculation
    df['MSI'] = df[['DVR','VOLZ','Absorption','Imbalance','Delta_Sequence','LVN','Wick_Trap','OI_Score']].mul(
        [2,1.5,1.2,1.5,1.0,0.8,1.2,1.5]).sum(axis=1).round(2)

    min_candle = int(df['Candle'].min())
    max_candle = int(df['Candle'].max())
    candle_range = st.sidebar.slider("Candle Range", min_candle, max_candle, (max_candle-5, max_candle))
    df_filtered = df[df['Candle'].between(*candle_range)]

    tabs = st.tabs(["📊 MSI Chart", "📉 Volume Profile", "📦 Footprint Viewer", "📈 Backtest Results"])

    with tabs[0]:
        st.subheader("MSI Overview")
        st.line_chart(df_filtered[['Timestamp', 'MSI']].set_index('Timestamp'))

    with tabs[1]:
        st.subheader("Volume Profile")
        plot_volume_profile(df_filtered)

    with tabs[2]:
        st.subheader("Footprint Viewer")
        for i in range(candle_range[0], candle_range[1]+1):
            st.markdown(f"**Candle {i}**")
            plot_footprint(df, index=i)

    with tabs[3]:
        st.subheader("Backtest Strategy")
        results, pnl_chart = run_backtest(df)
        st.dataframe(results, use_container_width=True)
        st.line_chart(pnl_chart.set_index("Timestamp"))

    if save_signals:
        fname = f"msi_signals_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df[df['MSI'].abs()>2.5][['Timestamp','Candle','MSI']].to_csv(fname, index=False)
        st.success(f"📁 MSI signals saved as {fname}")
else:
    st.info("Upload a CSV or Excel file with footprint + MSI data.")
