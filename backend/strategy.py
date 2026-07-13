import pandas as pd


class Strategy:

    @staticmethod
    def analyze(df: pd.DataFrame):

        row = df.iloc[-1]

        buy_score = 0
        sell_score = 0

        reasons_buy = []
        reasons_sell = []

        # ==========================================================
        # EMA
        # ==========================================================

        if row["EMA_9"] > row["EMA_21"] > row["EMA_50"] > row["EMA_100"]:

            buy_score += 10
            reasons_buy.append("EMA Trend")

        elif row["EMA_9"] < row["EMA_21"] < row["EMA_50"] < row["EMA_100"]:

            sell_score += 10
            reasons_sell.append("EMA Trend")

        # ==========================================================
        # SMA
        # ==========================================================

        if row["SMA_20"] > row["SMA_50"] > row["SMA_200"]:

            buy_score += 8
            reasons_buy.append("SMA Trend")

        elif row["SMA_20"] < row["SMA_50"] < row["SMA_200"]:

            sell_score += 8
            reasons_sell.append("SMA Trend")

        # ==========================================================
        # RSI
        # ==========================================================

        if 55 <= row["RSI"] <= 70:

            buy_score += 6
            reasons_buy.append("RSI")

        elif 30 <= row["RSI"] <= 45:

            sell_score += 6
            reasons_sell.append("RSI")

        # ==========================================================
        # MACD
        # ==========================================================

        if row["MACD"] > row["MACD_SIGNAL"]:

            buy_score += 8
            reasons_buy.append("MACD")

        else:

            sell_score += 8
            reasons_sell.append("MACD")

        # ==========================================================
        # ADX
        # ==========================================================

        if row["ADX"] > 25:

            if row["DI_PLUS"] > row["DI_MINUS"]:

                buy_score += 8
                reasons_buy.append("ADX")

            else:

                sell_score += 8
                reasons_sell.append("ADX")

        # ==========================================================
        # STOCHASTIC
        # ==========================================================

        if row["STOCH_K"] > row["STOCH_D"]:

            buy_score += 5
            reasons_buy.append("Stochastic")

        else:

            sell_score += 5
            reasons_sell.append("Stochastic")

        # ==========================================================
        # STOCH RSI
        # ==========================================================

        if row["STOCH_RSI"] > 0.5:

            buy_score += 4
            reasons_buy.append("Stoch RSI")

        else:

            sell_score += 4
            reasons_sell.append("Stoch RSI")

        # ==========================================================
        # CCI
        # ==========================================================

        if row["CCI"] > 100:

            buy_score += 4
            reasons_buy.append("CCI")

        elif row["CCI"] < -100:

            sell_score += 4
            reasons_sell.append("CCI")

        # ==========================================================
        # WILLIAMS %R
        # ==========================================================

        if row["WILLIAMS_R"] > -50:

            buy_score += 3
            reasons_buy.append("Williams %R")

        else:

            sell_score += 3
            reasons_sell.append("Williams %R")

        # ==========================================================
        # ROC
        # ==========================================================

        if row["ROC"] > 0:

            buy_score += 4
            reasons_buy.append("ROC")

        else:

            sell_score += 4
            reasons_sell.append("ROC")

        # ==========================================================
        # MFI
        # ==========================================================

        if row["MFI"] > 50:

            buy_score += 4
            reasons_buy.append("Money Flow")

        else:

            sell_score += 4
            reasons_sell.append("Money Flow")

        # ==========================================================
        # PSAR
        # ==========================================================

        if row["Close"] > row["PSAR"]:

            buy_score += 6
            reasons_buy.append("PSAR")

        else:

            sell_score += 6
            reasons_sell.append("PSAR")

        # ==========================================================
        # ICHIMOKU
        # ==========================================================

        if row["Close"] > row["ICHI_A"] and row["Close"] > row["ICHI_B"]:

            buy_score += 10
            reasons_buy.append("Ichimoku")

        else:

            sell_score += 10
            reasons_sell.append("Ichimoku")

        # ==========================================================
        # BOLLINGER
        # ==========================================================

        if row["Close"] > row["BB_MIDDLE"]:

            buy_score += 3
            reasons_buy.append("Bollinger")

        else:

            sell_score += 3
            reasons_sell.append("Bollinger")

        # ==========================================================
        # FINAL
        # ==========================================================

        total = buy_score + sell_score

        if total == 0:

            confidence = 0

        else:

            confidence = round(
                max(buy_score, sell_score) / total * 100
            )

        difference = buy_score - sell_score

        if difference >= 30:

            signal = "STRONG BUY"

        elif difference >= 15:

            signal = "BUY"

        elif difference <= -30:

            signal = "STRONG SELL"

        elif difference <= -15:

            signal = "SELL"

        else:

            signal = "WAIT"

        next_candle = "BULLISH" if difference > 0 else "BEARISH"

        return {

            "signal": signal,

            "confidence": confidence,

            "buy_score": buy_score,

            "sell_score": sell_score,

            "difference": difference,

            "next_candle": next_candle,

            "trade_quality": min(5, max(1, confidence // 20)),

            "reasons": reasons_buy if buy_score >= sell_score else reasons_sell

        }