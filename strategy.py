
import pandas as pd

def run_backtest(df):
    df = df.copy()
    df['Position'] = 0
    df.loc[df['MSI'] > 2.5, 'Position'] = 1
    df.loc[df['MSI'] < -2.5, 'Position'] = -1
    df['PnL'] = df['Position'].shift(1) * df['Delta']
    df['CumPnL'] = df['PnL'].cumsum()
    trades = df[df['Position'] != 0][['Timestamp', 'Candle', 'MSI', 'Position', 'PnL']]
    pnl_chart = df[['Timestamp', 'CumPnL']]
    return trades.tail(20), pnl_chart
