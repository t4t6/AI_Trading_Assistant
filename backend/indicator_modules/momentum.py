import pandas as pd


class MomentumAnalyzer:

    @staticmethod
    def analyze(row: pd.Series):

        buy = 0
        sell = 0

        reasons = []

        # ==========================================
        # RSI
        # ==========================================

        rsi = row["RSI"]

        if 55 <= rsi <= 70:

            buy += 8
            reasons.append("RSI Bullish Momentum")

        elif 30 <= rsi <= 45:

            sell += 8
            reasons.append("RSI Bearish Momentum")

        elif rsi < 30:

            buy += 4
            reasons.append("RSI Oversold")

        elif rsi > 70:

            sell += 4
            reasons.append("RSI Overbought")

        # ==========================================
        # MACD
        # ==========================================

        if row["MACD"] > row["MACD_SIGNAL"]:

            buy += 10
            reasons.append("MACD Bullish Cross")

        elif row["MACD"] < row["MACD_SIGNAL"]:

            sell += 10
            reasons.append("MACD Bearish Cross")

        # Histogram Strength

        if row["MACD_HIST"] > 0:

            buy += 3
            reasons.append("Positive MACD Histogram")

        elif row["MACD_HIST"] < 0:

            sell += 3
            reasons.append("Negative MACD Histogram")

        # ==========================================
        # STOCHASTIC
        # ==========================================

        if row["STOCH_K"] > row["STOCH_D"]:

            buy += 6
            reasons.append("Stochastic Bullish")

        elif row["STOCH_K"] < row["STOCH_D"]:

            sell += 6
            reasons.append("Stochastic Bearish")

        # ==========================================
        # STOCH RSI
        # ==========================================

        if row["STOCH_RSI"] > 0.8:

            buy += 3
            reasons.append("Strong Stoch RSI")

        elif row["STOCH_RSI"] < 0.2:

            sell += 3
            reasons.append("Weak Stoch RSI")

        # ==========================================
        # CCI
        # ==========================================

        if row["CCI"] > 100:

            buy += 5
            reasons.append("CCI Bullish")

        elif row["CCI"] < -100:

            sell += 5
            reasons.append("CCI Bearish")

        # ==========================================
        # Williams %R
        # ==========================================

        if row["WILLIAMS_R"] > -50:

            buy += 3
            reasons.append("Williams %R Bullish")

        else:

            sell += 3
            reasons.append("Williams %R Bearish")

        # ==========================================
        # ROC
        # ==========================================

        if row["ROC"] > 0:

            buy += 4
            reasons.append("Positive Rate of Change")

        elif row["ROC"] < 0:

            sell += 4
            reasons.append("Negative Rate of Change")

        return {

            "buy": buy,

            "sell": sell,

            "reasons": reasons

        }