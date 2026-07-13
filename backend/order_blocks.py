import pandas as pd


class OrderBlocks:

    IMPULSE_MULTIPLIER = 2.0

    LOOKAHEAD = 5

    @staticmethod
    def analyze(df: pd.DataFrame):

        buy = 0
        sell = 0

        reasons = []

        bullish_blocks = []
        bearish_blocks = []

        atr = float(df.iloc[-1]["ATR"])

        opens = df["Open"].tolist()
        highs = df["High"].tolist()
        lows = df["Low"].tolist()
        closes = df["Close"].tolist()

        current_price = closes[-1]

        # =====================================
        # Bullish Order Blocks
        # Last bearish candle before impulse
        # =====================================

        for i in range(10, len(df) - OrderBlocks.LOOKAHEAD):

            candle_low = lows[i]
            candle_high = highs[i]

            if closes[i] >= opens[i]:
                continue

            future_move = max(

                highs[
                    i + 1:
                    i + OrderBlocks.LOOKAHEAD + 1
                ]

            ) - closes[i]

            if future_move > atr * OrderBlocks.IMPULSE_MULTIPLIER:

                bullish_blocks.append({

                    "low": candle_low,

                    "high": candle_high,

                    "created": i,

                    "mitigated": False,

                    "strength": round(

                        future_move / atr,

                        2

                    )

                })

        # =====================================
        # Bearish Order Blocks
        # Last bullish candle before selloff
        # =====================================

        for i in range(10, len(df) - OrderBlocks.LOOKAHEAD):

            candle_low = lows[i]
            candle_high = highs[i]

            if closes[i] <= opens[i]:
                continue

            future_move = closes[i] - min(

                lows[
                    i + 1:
                    i + OrderBlocks.LOOKAHEAD + 1
                ]

            )

            if future_move > atr * OrderBlocks.IMPULSE_MULTIPLIER:

                bearish_blocks.append({

                    "low": candle_low,

                    "high": candle_high,

                    "created": i,

                    "mitigated": False,

                    "strength": round(

                        future_move / atr,

                        2

                    )

                })

        # =====================================
        # Mitigation Check
        # =====================================

        for block in bullish_blocks:

            for price in lows[block["created"] + 1:]:

                if block["low"] <= price <= block["high"]:

                    block["mitigated"] = True
                    break

        for block in bearish_blocks:

            for price in highs[block["created"] + 1:]:

                if block["low"] <= price <= block["high"]:

                    block["mitigated"] = True
                    break

        # =====================================
        # Nearest Bullish Block
        # =====================================

        nearest_bullish = None
        best_distance = float("inf")

        for block in bullish_blocks:

            if block["mitigated"]:
                continue

            distance = abs(

                current_price -

                block["high"]

            )

            if distance < best_distance:

                best_distance = distance
                nearest_bullish = block

        # =====================================
        # Nearest Bearish Block
        # =====================================

        nearest_bearish = None
        best_distance = float("inf")

        for block in bearish_blocks:

            if block["mitigated"]:
                continue

            distance = abs(

                current_price -

                block["low"]

            )

            if distance < best_distance:

                best_distance = distance
                nearest_bearish = block

        # =====================================
        # AI Score
        # =====================================

        if nearest_bullish:

            if (

                abs(

                    current_price -

                    nearest_bullish["high"]

                ) / current_price

            ) < 0.003:

                score = min(

                    20,

                    int(

                        nearest_bullish["strength"] * 4

                    )

                )

                buy += score

                reasons.append(

                    "Near Bullish Order Block"

                )

        if nearest_bearish:

            if (

                abs(

                    current_price -

                    nearest_bearish["low"]

                ) / current_price

            ) < 0.003:

                score = min(

                    20,

                    int(

                        nearest_bearish["strength"] * 4

                    )

                )

                sell += score

                reasons.append(

                    "Near Bearish Order Block"

                )

        return {

            "buy": buy,

            "sell": sell,

            "bullish_blocks": bullish_blocks,

            "bearish_blocks": bearish_blocks,

            "nearest_bullish": nearest_bullish,

            "nearest_bearish": nearest_bearish,

            "reasons": reasons

        }