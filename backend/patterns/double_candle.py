from .candle_utils import CandleUtils


class DoublePatterns:

    TOLERANCE = 0.001

    @staticmethod
    def detect(df):

        if len(df) < 2:

            return {

                "buy": 0,

                "sell": 0,

                "patterns": []

            }

        previous = df.iloc[-2]

        current = df.iloc[-1]

        buy = 0

        sell = 0

        patterns = []

        # ======================================
        # Bullish Engulfing
        # ======================================

        if (

            CandleUtils.bearish(previous)

            and

            CandleUtils.bullish(current)

            and

            current["Open"] <= previous["Close"]

            and

            current["Close"] >= previous["Open"]

        ):

            patterns.append(

                "Bullish Engulfing"

            )

            buy += 18

        # ======================================
        # Bearish Engulfing
        # ======================================

        if (

            CandleUtils.bullish(previous)

            and

            CandleUtils.bearish(current)

            and

            current["Open"] >= previous["Close"]

            and

            current["Close"] <= previous["Open"]

        ):

            patterns.append(

                "Bearish Engulfing"

            )

            sell += 18

        # ======================================
        # Bullish Harami
        # ======================================

        if (

            CandleUtils.bearish(previous)

            and

            CandleUtils.bullish(current)

            and

            current["Open"] > previous["Close"]

            and

            current["Close"] < previous["Open"]

        ):

            patterns.append(

                "Bullish Harami"

            )

            buy += 10

        # ======================================
        # Bearish Harami
        # ======================================

        if (

            CandleUtils.bullish(previous)

            and

            CandleUtils.bearish(current)

            and

            current["Open"] < previous["Close"]

            and

            current["Close"] > previous["Open"]

        ):

            patterns.append(

                "Bearish Harami"

            )

            sell += 10

        # ======================================
        # Tweezer Bottom
        # ======================================

        if abs(

            previous["Low"] -

            current["Low"]

        ) / previous["Low"] < DoublePatterns.TOLERANCE:

            if (

                CandleUtils.bearish(previous)

                and

                CandleUtils.bullish(current)

            ):

                patterns.append(

                    "Tweezer Bottom"

                )

                buy += 12

        # ======================================
        # Tweezer Top
        # ======================================

        if abs(

            previous["High"] -

            current["High"]

        ) / previous["High"] < DoublePatterns.TOLERANCE:

            if (

                CandleUtils.bullish(previous)

                and

                CandleUtils.bearish(current)

            ):

                patterns.append(

                    "Tweezer Top"

                )

                sell += 12

        # ======================================
        # Piercing Line
        # ======================================

        midpoint = (

            previous["Open"] +

            previous["Close"]

        ) / 2

        if (

            CandleUtils.bearish(previous)

            and

            CandleUtils.bullish(current)

            and

            current["Close"] > midpoint

            and

            current["Close"] < previous["Open"]

        ):

            patterns.append(

                "Piercing Line"

            )

            buy += 15

        # ======================================
        # Dark Cloud Cover
        # ======================================

        midpoint = (

            previous["Open"] +

            previous["Close"]

        ) / 2

        if (

            CandleUtils.bullish(previous)

            and

            CandleUtils.bearish(current)

            and

            current["Close"] < midpoint

            and

            current["Close"] > previous["Open"]

        ):

            patterns.append(

                "Dark Cloud Cover"

            )

            sell += 15

        # ======================================
        # Inside Bar
        # ======================================

        if (

            current["High"] < previous["High"]

            and

            current["Low"] > previous["Low"]

        ):

            patterns.append(

                "Inside Bar"

            )

        # ======================================
        # Outside Bar
        # ======================================

        if (

            current["High"] > previous["High"]

            and

            current["Low"] < previous["Low"]

        ):

            patterns.append(

                "Outside Bar"

            )

        return {

            "buy": buy,

            "sell": sell,

            "patterns": patterns

        }