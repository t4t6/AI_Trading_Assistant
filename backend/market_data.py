import time
import requests
import pandas as pd
import yfinance as yf

from assets import get_asset_info

BINANCE_KLINES_URL = "https://api.binance.com/api/v3/klines"

# Binance interval strings line up 1:1 with our timeframe names
BINANCE_INTERVALS = {"1m", "3m", "5m", "15m", "30m", "1h", "4h", "1d"}

# yfinance (period, interval) per requested timeframe.
# yfinance has no native 3m or 4h interval, so those are derived below.
YF_INTERVAL_MAP = {
    "1m": ("7d", "1m"),
    "3m": ("60d", "5m"),    # approximated from 5m bars (Yahoo has no 3m)
    "5m": ("60d", "5m"),
    "15m": ("60d", "15m"),
    "30m": ("60d", "30m"),
    "1h": ("730d", "1h"),
    "4h": ("730d", "1h"),   # resampled to true 4h candles below
    "1d": ("10y", "1d"),
}


class MarketData:
    """
    Single entry point for OHLCV data.
    Routes crypto -> Binance (truly live, no key).
    Routes forex/commodities -> Yahoo Finance (free, delayed ~15min on many symbols).
    Always returns a DataFrame with columns: Open, High, Low, Close, Volume
    """

    @staticmethod
    def get_data(symbol, timeframe):
        info = get_asset_info(symbol)
        if info is None:
            return None

        if info["source"] == "binance":
            return MarketData._from_binance(info["fetch"], timeframe)
        else:
            return MarketData._from_yfinance(info["fetch"], timeframe)

    # ------------------------------------------------------------------
    # Binance — real-time, no API key required
    # ------------------------------------------------------------------
    @staticmethod
    def _from_binance(fetch_symbol, timeframe):
        interval = timeframe if timeframe in BINANCE_INTERVALS else "1h"

        params = {
            "symbol": fetch_symbol,
            "interval": interval,
            "limit": 500,
        }

        resp = requests.get(BINANCE_KLINES_URL, params=params, timeout=10)
        resp.raise_for_status()
        raw = resp.json()

        if not raw:
            return None

        df = pd.DataFrame(raw, columns=[
            "open_time", "Open", "High", "Low", "Close", "Volume",
            "close_time", "quote_asset_volume", "trades",
            "taker_buy_base", "taker_buy_quote", "ignore"
        ])

        for col in ["Open", "High", "Low", "Close", "Volume"]:
            df[col] = df[col].astype(float)

        df = df[["Open", "High", "Low", "Close", "Volume"]].reset_index(drop=True)
        return df

    # ------------------------------------------------------------------
    # Yahoo Finance — free, no key, delayed for many symbols
    # ------------------------------------------------------------------
    @staticmethod
    def _from_yfinance(fetch_symbol, timeframe):
        period, interval = YF_INTERVAL_MAP.get(timeframe, ("730d", "1h"))

        df = yf.download(
            fetch_symbol,
            period=period,
            interval=interval,
            auto_adjust=True,
            progress=False,
        )

        if df is None or len(df) == 0:
            return None

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        if timeframe == "4h":
            df = df.resample("4h").agg({
                "Open": "first",
                "High": "max",
                "Low": "min",
                "Close": "last",
                "Volume": "sum",
            }).dropna()

        df = df.reset_index(drop=True)
        return df
