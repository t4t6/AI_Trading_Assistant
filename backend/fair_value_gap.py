import pandas as pd


class FairValueGap:

    FILL_TOLERANCE = 0.15

    @staticmethod
    def analyze(df: pd.DataFrame):

        bullish_gaps = []

        bearish_gaps = []

        buy = 0

        sell = 0

        reasons = []

        if len(df) < 5:

            return {

                "buy": 0,

                "sell": 0,

                "bullish_gaps": [],

                "bearish_gaps": [],

                "nearest_bullish": None,

                "nearest_bearish": None,

                "reasons": []

            }

        highs = df["High"].tolist()

        lows = df["Low"].tolist()

        closes = df["Close"].tolist()

        current_price = float(closes[-1])

        # =====================================
        # Detect Bullish FVG
        # Candle1 High < Candle3 Low
        # =====================================

        for i in range(2, len(df)):

            first_high = highs[i - 2]

            third_low = lows[i]

            if third_low > first_high:

                bullish_gaps.append({

                    "start": first_high,

                    "end": third_low,

                    "index": i,

                    "filled": False

                })

        # =====================================
        # Detect Bearish FVG
        # Candle1 Low > Candle3 High
        # =====================================

        for i in range(2, len(df)):

            first_low = lows[i - 2]

            third_high = highs[i]

            if third_high < first_low:

                bearish_gaps.append({

                    "start": third_high,

                    "end": first_low,

                    "index": i,

                    "filled": False

                })

        # =====================================
        # Check Filled Gaps
        # =====================================

        for gap in bullish_gaps:

            gap_size = gap["end"] - gap["start"]

            fill_level = gap["start"] + (

                gap_size *

                FairValueGap.FILL_TOLERANCE

            )

            if current_price <= fill_level:

                gap["filled"] = True

        for gap in bearish_gaps:

            gap_size = gap["end"] - gap["start"]

            fill_level = gap["end"] - (

                gap_size *

                FairValueGap.FILL_TOLERANCE

            )

            if current_price >= fill_level:

                gap["filled"] = True

        # =====================================
        # Nearest Bullish Gap
        # =====================================

        nearest_bullish = None

        nearest_distance = 999999999

        for gap in bullish_gaps:

            if gap["filled"]:

                continue

            midpoint = (

                gap["start"] +

                gap["end"]

            ) / 2

            distance = abs(

                current_price -

                midpoint

            )

            if distance < nearest_distance:

                nearest_distance = distance

                nearest_bullish = gap

        # =====================================
        # Nearest Bearish Gap
        # =====================================

        nearest_bearish = None

        nearest_distance = 999999999

        for gap in bearish_gaps:

            if gap["filled"]:

                continue

            midpoint = (

                gap["start"] +

                gap["end"]

            ) / 2

            distance = abs(

                current_price -

                midpoint

            )

            if distance < nearest_distance:

                nearest_distance = distance

                nearest_bearish = gap

        # =====================================
        # AI Score
        # =====================================

        if nearest_bullish:

            midpoint = (

                nearest_bullish["start"] +

                nearest_bullish["end"]

            ) / 2

            if abs(current_price - midpoint) / current_price < 0.003:

                buy += 12

                reasons.append(

                    "Price Near Bullish Fair Value Gap"

                )

        if nearest_bearish:

            midpoint = (

                nearest_bearish["start"] +

                nearest_bearish["end"]

            ) / 2

            if abs(current_price - midpoint) / current_price < 0.003:

                sell += 12

                reasons.append(

                    "Price Near Bearish Fair Value Gap"

                )

        return {

            "buy": buy,

            "sell": sell,

            "bullish_gaps": bullish_gaps,

            "bearish_gaps": bearish_gaps,

            "nearest_bullish": nearest_bullish,

            "nearest_bearish": nearest_bearish,

            "reasons": reasons

        }