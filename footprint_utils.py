
import streamlit as st
import plotly.graph_objects as go

def plot_footprint(df, index=0):
    candle = df[df['Candle']==index]
    if candle.empty:
        st.warning(f"No data for Candle {index}")
        return
    fig = go.Figure()
    for _, row in candle.iterrows():
        price = row['Price']
        bid = row['Bid_Vol']
        ask = row['Ask_Vol']
        fig.add_trace(go.Bar(x=[bid], y=[price], orientation='h', marker_color='blue', showlegend=False))
        fig.add_trace(go.Bar(x=[-ask], y=[price], orientation='h', marker_color='red', showlegend=False))
    fig.update_layout(barmode='overlay', yaxis=dict(autorange='reversed'), height=300)
    st.plotly_chart(fig, use_container_width=True)

def plot_volume_profile(df):
    prof = df.groupby('Price')['Volume'].sum().reset_index().sort_values('Volume')
    fig = go.Figure(go.Bar(x=prof['Volume'], y=prof['Price'], orientation='h', marker_color='orange'))
    fig.update_layout(height=500, xaxis_title="Volume", yaxis_title="Price")
    st.plotly_chart(fig, use_container_width=True)
