import yfinance as yf
import polars as pl
import os


TICKERS = ["PETR4.SA", "VALE3.SA", "AAPL34.SA"]

for ticker in TICKERS:
    df = yf.download(ticker, period="15d", interval="1d", multi_level_index=False)
    df.reset_index(inplace=True)
    df = pl.from_pandas(df)
    if df.empty:
        continue  # pula se nÃ£o houver dados
