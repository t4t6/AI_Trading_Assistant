from datetime import datetime, timedelta

from market_data import MarketData


class DataManager:

    _cache = {}

    _expiry = {

        "1m": 30,
        "3m": 60,
        "5m": 90,
        "15m": 180,
        "30m": 300,
        "1h": 600,
        "4h": 1800,
        "1d": 3600

    }

    @classmethod
    def get_data(cls, symbol, interval):

        key = f"{symbol}_{interval}"

        now = datetime.now()

        if key in cls._cache:

            cached = cls._cache[key]

            age = (
                now -
                cached["time"]
            ).total_seconds()

            if age < cls._expiry.get(interval, 60):

                return cached["data"]

        df = MarketData.get_data(

            symbol=symbol,

            interval=interval

        )

        cls._cache[key] = {

            "time": now,

            "data": df

        }

        return df

    @classmethod
    def clear_cache(cls):

        cls._cache.clear()

    @classmethod
    def cache_size(cls):

        return len(cls._cache)

    @classmethod
    def remove(cls, symbol, interval):

        key = f"{symbol}_{interval}"

        if key in cls._cache:

            del cls._cache[key]

    @classmethod
    def preload(

        cls,

        symbols,

        intervals

    ):

        for symbol in symbols:

            for interval in intervals:

                try:

                    cls.get_data(

                        symbol,

                        interval

                    )

                except Exception:

                    pass