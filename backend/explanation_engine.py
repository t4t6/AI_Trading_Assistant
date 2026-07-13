class ExplanationEngine:

    @staticmethod
    def generate(signal_data):

        reasons = []

        # --------------------------
        # EMA Trend
        # --------------------------

        if (
            signal_data["ema_9"] >
            signal_data["ema_21"] >
            signal_data["ema_50"]
        ):

            reasons.append(
                "EMA 9 is above EMA 21 and EMA 50 (Strong Bullish Trend)"
            )

        elif (
            signal_data["ema_9"] <
            signal_data["ema_21"] <
            signal_data["ema_50"]
        ):

            reasons.append(
                "EMA 9 is below EMA 21 and EMA 50 (Strong Bearish Trend)"
            )

        else:

            reasons.append(
                "EMA trend is mixed."
            )

        # --------------------------
        # RSI
        # --------------------------

        rsi = signal_data["rsi"]

        if rsi < 30:

            reasons.append(
                f"RSI = {rsi:.2f} (Oversold)"
            )

        elif rsi > 70:

            reasons.append(
                f"RSI = {rsi:.2f} (Overbought)"
            )

        else:

            reasons.append(
                f"RSI = {rsi:.2f} (Neutral)"
            )

        # --------------------------
        # MACD
        # --------------------------

        if signal_data["macd"] > signal_data["macd_signal"]:

            reasons.append(
                "MACD is above the Signal Line."
            )

        else:

            reasons.append(
                "MACD is below the Signal Line."
            )

        # --------------------------
        # Confidence
        # --------------------------

        confidence = signal_data["confidence"]

        if confidence >= 90:

            risk = "Very Low"

        elif confidence >= 75:

            risk = "Low"

        elif confidence >= 60:

            risk = "Medium"

        elif confidence >= 40:

            risk = "High"

        else:

            risk = "Very High"

        # --------------------------
        # Trend Strength
        # --------------------------

        score = signal_data["score"]

        if score >= 5:

            trend = "Very Strong Bullish"

        elif score >= 3:

            trend = "Bullish"

        elif score <= -5:

            trend = "Very Strong Bearish"

        elif score <= -3:

            trend = "Bearish"

        else:

            trend = "Sideways"

        # --------------------------
        # Holding Time
        # --------------------------

        timeframe = signal_data["timeframe"]

        holding = {

            "1m": "1 - 5 Minutes",

            "2m": "2 - 10 Minutes",

            "5m": "5 - 20 Minutes",

            "15m": "15 - 60 Minutes",

            "30m": "30 Minutes - 2 Hours",

            "1h": "1 - 6 Hours",

            "4h": "4 Hours - 2 Days",

            "1d": "2 Days - 2 Weeks"

        }.get(timeframe, "Unknown")

        return {

            "reasons": reasons,

            "risk": risk,

            "trend": trend,

            "holding_time": holding

        }