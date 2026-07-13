import pandas as pd


class VolatilityAnalyzer:

    @staticmethod
    def analyze(df: pd.DataFrame):

        row = df.iloc[-1]

        buy = 0
        sell = 0

        reasons = []

        # ==================================================
        # ATR
        # ==================================================

        atr = float(row["ATR"])
        price = float(row["Close"])

        atr_percent = (atr / price) * 100

        if 0.20 <= atr_percent <= 2.50:

            buy += 5
            sell += 5

            reasons.append("Healthy Volatility")

        elif atr_percent < 0.20:

            reasons.append("Low Volatility")

        else:

            reasons.append("High Volatility")

        # ==================================================
        # Bollinger Bands
        # ==================================================

        upper = float(row["BB_UPPER"])
        lower = float(row["BB_LOWER"])
        middle = float(row["BB_MIDDLE"])

        if price > middle:

            buy += 3
            reasons.append("Price Above Bollinger Midline")

        elif price < middle:

            sell += 3
            reasons.append("Price Below Bollinger Midline")

        if price <= lower:

            buy += 6
            reasons.append("Lower Bollinger Reversal Zone")

        elif price >= upper:

            sell += 6
            reasons.append("Upper Bollinger Reversal Zone")

        # ==================================================
        # Donchian Channel
        # ==================================================

        dc_high = float(row["DONCHIAN_HIGH"])
        dc_low = float(row["DONCHIAN_LOW"])

        if price >= dc_high:

            buy += 5
            reasons.append("Donchian Breakout Up")

        elif price <= dc_low:

            sell += 5
            reasons.append("Donchian Breakout Down")

        # ==================================================
        # Keltner Channel
        # ==================================================

        kc_upper = float(row["KC_UPPER"])
        kc_middle = float(row["KC_MIDDLE"])
        kc_lower = float(row["KC_LOWER"])

        if price > kc_middle:

            buy += 2
            reasons.append("Above Keltner Midline")

        elif price < kc_middle:

            sell += 2
            reasons.append("Below Keltner Midline")

        if price > kc_upper:

            buy += 4
            reasons.append("Bullish Keltner Breakout")

        elif price < kc_lower:

            sell += 4
            reasons.append("Bearish Keltner Breakdown")

        # ==================================================
        # Volatility Rating
        # ==================================================

        if atr_percent < 0.20:

            volatility = "LOW"

        elif atr_percent < 0.80:

            volatility = "NORMAL"

        elif atr_percent < 2.50:

            volatility = "HIGH"

        else:

            volatility = "EXTREME"

        return {

            "buy": buy,

            "sell": sell,

            "volatility": volatility,

            "atr_percent": round(atr_percent, 2),

            "reasons": reasons

        }