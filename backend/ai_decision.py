class AIDecision:

    @staticmethod
    def generate(strategy, explanation):

        score = strategy["score"]

        confidence = strategy["confidence"]

        # -----------------------------------
        # Signal Strength
        # -----------------------------------

        if score >= 6:

            signal = "STRONG BUY"

        elif score >= 3:

            signal = "BUY"

        elif score >= 1:

            signal = "WEAK BUY"

        elif score <= -6:

            signal = "STRONG SELL"

        elif score <= -3:

            signal = "SELL"

        elif score <= -1:

            signal = "WEAK SELL"

        else:

            signal = "WAIT"

        # -----------------------------------
        # Binary Candle Prediction
        # -----------------------------------

        if score >= 2:

            candle = "BULLISH"

            candle_probability = min(
                confidence + 5,
                99
            )

        elif score <= -2:

            candle = "BEARISH"

            candle_probability = min(
                confidence + 5,
                99
            )

        else:

            candle = "NEUTRAL"

            candle_probability = 50

        # -----------------------------------
        # Trade Quality
        # -----------------------------------

        if confidence >= 90:

            stars = "★★★★★"

        elif confidence >= 80:

            stars = "★★★★☆"

        elif confidence >= 70:

            stars = "★★★☆☆"

        elif confidence >= 60:

            stars = "★★☆☆☆"

        else:

            stars = "★☆☆☆☆"

        return {

            "signal": signal,

            "confidence": confidence,

            "next_candle": candle,

            "next_candle_probability": candle_probability,

            "trade_quality": stars,

            "risk": explanation["risk"],

            "trend": explanation["trend"],

            "holding_time": explanation["holding_time"],

            "why": explanation["reasons"]

        }