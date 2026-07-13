import numpy as np
import pandas as pd


class SupportResistance:

    SWING = 6

    MERGE_DISTANCE = 0.0025

    @staticmethod
    def _merge(levels, distance):

        merged = []

        for level in sorted(levels):

            if not merged:

                merged.append(level)

                continue

            if abs(level - merged[-1]) / merged[-1] <= distance:

                merged[-1] = (merged[-1] + level) / 2

            else:

                merged.append(level)

        return merged

    @staticmethod
    def analyze(df: pd.DataFrame):

        highs = df["High"].to_numpy()

        lows = df["Low"].to_numpy()

        close = float(df.iloc[-1]["Close"])

        supports = []

        resistances = []

        swing = SupportResistance.SWING

        for i in range(swing, len(df) - swing):

            low = lows[i]

            if low == np.min(

                lows[i-swing:i+swing+1]

            ):

                supports.append(low)

        for i in range(swing, len(df) - swing):

            high = highs[i]

            if high == np.max(

                highs[i-swing:i+swing+1]

            ):

                resistances.append(high)

        supports = SupportResistance._merge(

            supports,

            SupportResistance.MERGE_DISTANCE

        )

        resistances = SupportResistance._merge(

            resistances,

            SupportResistance.MERGE_DISTANCE

        )

        nearest_support = None

        nearest_resistance = None

        below = [

            s for s in supports

            if s <= close

        ]

        above = [

            r for r in resistances

            if r >= close

        ]

        if below:

            nearest_support = max(below)

        if above:

            nearest_resistance = min(above)

        support_strength = 0

        resistance_strength = 0

        for s in supports:

            if abs(close - s) / close < 0.003:

                support_strength += 1

        for r in resistances:

            if abs(close - r) / close < 0.003:

                resistance_strength += 1

        if nearest_support:

            support_distance = round(

                abs(close - nearest_support),

                6

            )

        else:

            support_distance = None

        if nearest_resistance:

            resistance_distance = round(

                abs(nearest_resistance - close),

                6

            )

        else:

            resistance_distance = None

        breakout = False

        breakdown = False

        if nearest_resistance:

            if close > nearest_resistance:

                breakout = True

        if nearest_support:

            if close < nearest_support:

                breakdown = True

        score_buy = 0

        score_sell = 0

        reasons = []

        if breakout:

            score_buy += 20

            reasons.append(

                "Resistance Breakout"

            )

        if breakdown:

            score_sell += 20

            reasons.append(

                "Support Breakdown"

            )

        if support_distance is not None:

            if support_distance < close * 0.002:

                score_buy += 8

                reasons.append(

                    "Price Near Strong Support"

                )

        if resistance_distance is not None:

            if resistance_distance < close * 0.002:

                score_sell += 8

                reasons.append(

                    "Price Near Strong Resistance"

                )

        return {

            "buy": score_buy,

            "sell": score_sell,

            "supports": supports,

            "resistances": resistances,

            "nearest_support": nearest_support,

            "nearest_resistance": nearest_resistance,

            "support_strength": support_strength,

            "resistance_strength": resistance_strength,

            "support_distance": support_distance,

            "resistance_distance": resistance_distance,

            "breakout": breakout,

            "breakdown": breakdown,

            "reasons": reasons

        }