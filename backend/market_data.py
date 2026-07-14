import os
import logging
import requests
import pandas as pd

from assets import get_asset_info

TWELVEDATA_URL = "https://api.twelvedata.com/time_series"
TWELVEDATA_API_KEY = os.environ.get("TWELVEDATA_API_KEY", "")

# Our timeframe name -> Twelve Data interval string
TD_INTERVAL_MAP = {
    "1m": "1min",
    "3m": None,      # not natively supported, derived by resampling 1min bars below
    "5m": "5min",
    "15m": "15min",
    "30m": "30min",
    "1h": "1h",
    "4h": "4h",
    "1d": "1day",
}


class MarketData:
    """
    Single entry point for OHLCV data — everything routes through Twelve Data
    (forex, commodities, and crypto), since free cloud hosts are frequently
    blocked by Yahoo Finance and by Binance's US-region restriction.
    Always returns a DataFrame with columns: Open, High, Low, Close, Volume
    """

    @staticmethod
    def get_data(symbol, timeframe):
        info = get_asset_info(symbol)
        if info is None:
            return None

        return MarketData._from_twelvedata(info["fetch"], timeframe)

    @staticmethod
    def _from_twelvedata(fetch_symbol, timeframe):
        if not TWELVEDATA_API_KEY:
            logging.error("TWELVEDATA_API_KEY is not set on the server.")
            return None

        interval = TD_INTERVAL_MAP.get(timeframe, "1h")
        needs_resample = interval is None
        query_interval = "1min" if needs_resample else interval

        params = {
            "symbol": fetch_symbol,
            "interval": query_interval,
            "outputsize": 1000 if needs_resample else 500,
            "apikey": TWELVEDATA_API_KEY,
        }

        try:
            resp = requests.get(TWELVEDATA_URL, params=params, timeout=15)
            data = resp.json()
        except Exception as e:
            logging.error(f"Twelve Data request failed for {fetch_symbol}: {e}")
            return None

        if data.get("status") == "error" or "values" not in data:
            logging.error(f"Twelve Data error for {fetch_symbol}: {data.get('message', data)}")
            return None

        values = data["values"]
        if not values:
            return None

        df = pd.DataFrame(values)
        df = df.rename(columns={
            "open": "Open", "high": "High", "low": "Low",
            "close": "Close", "volume": "Volume",
        })

        for col in ["Open", "High", "Low", "Close"]:
            df[col] = df[col].astype(float)
        df["Volume"] = df["Volume"].astype(float) if "Volume" in df.columns else 0.0

        # Twelve Data returns newest-first; flip to chronological order
        df = df.iloc[::-1].reset_index(drop=True)

        if needs_resample:
            df["datetime"] = pd.to_datetime([v["datetime"] for v in values[::-1]])
            df = df.set_index("datetime").resample("3min").agg({
                "Open": "first", "High": "max", "Low": "min",
                "Close": "last", "Volume": "sum",
            }).dropna().reset_index(drop=True)

        return df
