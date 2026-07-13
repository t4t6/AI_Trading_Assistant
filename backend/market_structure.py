import pandas as pd
import numpy as np


class MarketStructure:

    SWING_LOOKBACK = 5

    @staticmethod
    def analyze(df: pd.DataFrame):

        highs = df["High"].values
        lows = df["Low"].values

        swing_highs = []
        swing_lows = []

        lookback = MarketStructure.SWING_LOOKBACK

        # ----------------------------
        # Swing Highs
        # ----------------------------

        for i in range(lookback, len(df) - lookback):

            if highs[i] == max(highs[i-lookback:i+lookback+1]):

                swing_highs.append(i)

        # ----------------------------
        # Swing Lows
        # ----------------------------

        for i in range(lookback, len(df) - lookback):

            if lows[i] == min(lows[i-lookback:i+lookback+1]):

                swing_lows.append(i)

        # ----------------------------
        # Trend
        # ----------------------------

        trend = "RANGE"

        if len(swing_highs) >= 2 and len(swing_lows) >= 2:

            last_high = highs[swing_highs[-1]]
            prev_high = highs[swing_highs[-2]]

            last_low = lows[swing_lows[-1]]
            prev_low = lows[swing_lows[-2]]

            if last_high > prev_high and last_low > prev_low:

                trend = "UPTREND"

            elif last_high < prev_high and last_low < prev_low:

                trend = "DOWNTREND"

        # ----------------------------
        # Break of Structure
        # ----------------------------

        bos = False

        bos_direction = "NONE"

        close = float(df.iloc[-1]["Close"])

        if swing_highs:

            if close > highs[swing_highs[-1]]:

                bos = True

                bos_direction = "BULLISH"

        if swing_lows:

            if close < lows[swing_lows[-1]]:

                bos = True

                bos_direction = "BEARISH"

        # ----------------------------
        # Change of Character
        # ----------------------------

        choch = False

        if trend == "UPTREND" and bos_direction == "BEARISH":

            choch = True

        elif trend == "DOWNTREND" and bos_direction == "BULLISH":

            choch = True

        return {

            "trend": trend,

            "bos": bos,

            "bos_direction": bos_direction,

            "choch": choch,

            "swing_highs": swing_highs,

            "swing_lows": swing_lows

        }