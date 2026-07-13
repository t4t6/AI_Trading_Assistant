class AIScorer:

    @staticmethod
    def calculate(

        trend,
        momentum,
        volatility,
        volume,
        mtf

    ):

        buy = (
            trend["buy"] +
            momentum["buy"] +
            volatility["buy"] +
            volume["buy"] +
            mtf["buy"]
        )

        sell = (
            trend["sell"] +
            momentum["sell"] +
            volatility["sell"] +
            volume["sell"] +
            mtf["sell"]
        )

        difference = buy - sell

        total = buy + sell

        if total == 0:
            confidence = 0
        else:
            confidence = round(
                (max(buy, sell) / total) * 100
            )

        # =====================================
        # Signal
        # =====================================

        if difference >= 40:

            signal = "STRONG BUY"

        elif difference >= 20:

            signal = "BUY"

        elif difference <= -40:

            signal = "STRONG SELL"

        elif difference <= -20:

            signal = "SELL"

        else:

            signal = "WAIT"

        # =====================================
        # Binary
        # =====================================

        if difference > 0:

            next_candle = "BULLISH"

        elif difference < 0:

            next_candle = "BEARISH"

        else:

            next_candle = "NEUTRAL"

        # =====================================
        # Trade Quality
        # =====================================

        if confidence >= 90:

            stars = 5

        elif confidence >= 80:

            stars = 4

        elif confidence >= 70:

            stars = 3

        elif confidence >= 60:

            stars = 2

        else:

            stars = 1

        # =====================================
        # Reasons
        # =====================================

        reasons = []

        reasons.extend(trend["reasons"][:3])

        reasons.extend(momentum["reasons"][:3])

        reasons.extend(volatility["reasons"][:2])

        reasons.extend(volume["reasons"][:2])

        if mtf["overall"] == "BULLISH":

            reasons.append(
                "Multi-Timeframe Bullish Confirmation"
            )

        elif mtf["overall"] == "BEARISH":

            reasons.append(
                "Multi-Timeframe Bearish Confirmation"
            )

        return {

            "signal": signal,

            "confidence": confidence,

            "buy_score": buy,

            "sell_score": sell,

            "difference": difference,

            "next_candle": next_candle,

            "trade_quality": stars,

            "reasons": reasons

        }