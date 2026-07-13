import pandas as pd


class VolumeAnalyzer:

    @staticmethod
    def analyze(df: pd.DataFrame):

        row = df.iloc[-1]

        buy = 0
        sell = 0

        reasons = []

        # ============================================
        # On Balance Volume (OBV)
        # ============================================

        if len(df) >= 2:

            previous_obv = float(df.iloc[-2]["OBV"])
            current_obv = float(row["OBV"])

            if current_obv > previous_obv:

                buy += 8
                reasons.append("OBV Rising")

            elif current_obv < previous_obv:

                sell += 8
                reasons.append("OBV Falling")

        # ============================================
        # Money Flow Index (MFI)
        # ============================================

        mfi = float(row["MFI"])

        if 50 <= mfi <= 80:

            buy += 6
            reasons.append("Positive Money Flow")

        elif 20 <= mfi < 50:

            sell += 6
            reasons.append("Negative Money Flow")

        elif mfi < 20:

            buy += 3
            reasons.append("Money Flow Oversold")

        elif mfi > 80:

            sell += 3
            reasons.append("Money Flow Overbought")

        # ============================================
        # Volume Trend
        # ============================================

        recent_volume = df["Volume"].tail(20).mean()
        current_volume = float(row["Volume"])

        if recent_volume > 0:

            volume_ratio = current_volume / recent_volume

        else:

            volume_ratio = 1.0

        if volume_ratio >= 1.50:

            buy += 5
            sell += 5

            reasons.append("High Trading Volume")

        elif volume_ratio <= 0.70:

            buy -= 2
            sell -= 2

            reasons.append("Weak Trading Volume")

        # ============================================
        # Price + Volume Confirmation
        # ============================================

        if len(df) >= 2:

            previous_close = float(df.iloc[-2]["Close"])
            current_close = float(row["Close"])

            if current_close > previous_close and volume_ratio > 1:

                buy += 6
                reasons.append("Bullish Price/Volume Confirmation")

            elif current_close < previous_close and volume_ratio > 1:

                sell += 6
                reasons.append("Bearish Price/Volume Confirmation")

        # ============================================
        # Volume Rating
        # ============================================

        if volume_ratio >= 2.0:

            rating = "VERY HIGH"

        elif volume_ratio >= 1.2:

            rating = "HIGH"

        elif volume_ratio >= 0.8:

            rating = "NORMAL"

        else:

            rating = "LOW"

        return {

            "buy": buy,

            "sell": sell,

            "volume_ratio": round(volume_ratio, 2),

            "volume_rating": rating,

            "reasons": reasons

        }