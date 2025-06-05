import numpy as np
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from datetime import datetime, timedelta
import yfinance as yf
import polars as pl
import os

DEFAULT_ARGS = {
    "owner": "airflow",
}

TICKERS = ["PETR4.SA", "VALE3.SA", "AAPL34.SA"]
DATA_PATH = "/opt/airflow/data"

# Task 1: Buscar dados
def fetch_data():
    os.makedirs(DATA_PATH, exist_ok=True)
    for ticker in TICKERS:
        df = yf.download(ticker, period="15d", interval="1d", progress=False, auto_adjust=True, multi_level_index=False)
        # df.reset_index(inplace=True)
        if df.empty:
            continue

        df.to_parquet(f"{DATA_PATH}/{ticker.replace('.', '_')}_raw.parquet", index=False)

# Task 2: Processar dados
def process_data():
    for ticker in TICKERS:
        path = f"{DATA_PATH}/{ticker.replace('.', '_')}_raw.parquet"
        if not os.path.exists(path):
            continue

        pl_df = pl.read_parquet(path)
        print(pl_df.head())

        pl_df = pl_df.with_columns([
            pl.lit(ticker).alias("Ticker"),
            pl_df["Close"].pct_change().alias("Daily Return")
        ])

        daily_returns = pl_df["Daily Return"].to_numpy()
        cumulative_returns = np.cumprod(1 + np.nan_to_num(daily_returns, nan=0.0))

        pl_df = pl_df.with_columns([
            pl.Series(name="Cumulative Return", values=cumulative_returns),
            pl_df["Close"].rolling_mean(7).alias("MA_7"),
            pl_df["Daily Return"].rolling_std(7).alias("Volatility_7d"),
            pl_df["Volume"].rolling_mean(7).alias("Volume_MA_7")
        ])

        # Salva em Parquet e CSV
        pl_df.write_parquet(f"{DATA_PATH}/{ticker.replace('.', '_')}_processed.parquet")
        pl_df.write_csv(f"{DATA_PATH}/{ticker.replace('.', '_')}_processed.csv")

with DAG(
    dag_id="fetch_stock_prices_polars",
    default_args=DEFAULT_ARGS,
    schedule="0 18 * * 1-5",  # Segunda a sexta, 18h
    start_date=datetime(2024, 1, 1),
    catchup=False,
    is_paused_upon_creation=True,
    tags={"stocks", "finance", "polars"}
) as dag:

    start = EmptyOperator(task_id="start")

    fetch_task = PythonOperator(
        task_id="fetch_data",
        python_callable=fetch_data
    )

    process_task = PythonOperator(
        task_id="process_data",
        python_callable=process_data
    )

    end = EmptyOperator(task_id="end")

    start >> fetch_task >> process_task >> end
