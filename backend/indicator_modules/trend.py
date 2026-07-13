import pandas as pd


class TrendAnalyzer:

    @staticmethod
    def analyze(row: pd.Series):

        buy = 0
        sell = 0

        reasons = []

        # EMA Trend

        if row["EMA_9"] > row["EMA_21"] > row["EMA_50"]:

            buy += 10

            reasons.append("EMA Bullish Alignment")

        elif row["EMA_9"] < row["EMA_21"] < row["EMA_50"]:

            sell += 10

            reasons.append("EMA Bearish Alignment")

        # Long Trend

        if row["EMA_50"] > row["EMA_100"] > row["EMA_200"]:

            buy += 12

            reasons.append("Long-Term Uptrend")

        elif row["EMA_50"] < row["EMA_100"] < row["EMA_200"]:

            sell += 12

            reasons.append("Long-Term Downtrend")

        # SMA Trend

        if row["SMA_20"] > row["SMA_50"] > row["SMA_200"]:

            buy += 8

            reasons.append("SMA Bullish")

        elif row["SMA_20"] < row["SMA_50"] < row["SMA_200"]:

            sell += 8

            reasons.append("SMA Bearish")

        # ADX

        if row["ADX"] >= 25:

            if row["DI_PLUS"] > row["DI_MINUS"]:

                buy += 8

                reasons.append("Strong Uptrend")

            else:

                sell += 8

                reasons.append("Strong Downtrend")

        # Ichimoku

        if row["Close"] > row["ICHI_A"] and row["Close"] > row["ICHI_B"]:

            buy += 10

            reasons.append("Above Ichimoku Cloud")

        elif row["Close"] < row["ICHI_A"] and row["Close"] < row["ICHI_B"]:

            sell += 10

            reasons.append("Below Ichimoku Cloud")

        return {

            "buy": buy,

            "sell": sell,

            "reasons": reasons

        }