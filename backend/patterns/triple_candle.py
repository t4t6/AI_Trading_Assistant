from .candle_utils import CandleUtils


class TriplePatterns:

    @staticmethod
    def detect(df):

        if len(df) < 3:

            return {

                "buy": 0,

                "sell": 0,

                "patterns": []

            }

        c1 = df.iloc[-3]
        c2 = df.iloc[-2]
        c3 = df.iloc[-1]

        buy = 0
        sell = 0

        patterns = []

        # =====================================
        # Morning Star
        # =====================================

        midpoint = (

            c1["Open"] +

            c1["Close"]

        ) / 2

        if (

            CandleUtils.bearish(c1)

            and

            CandleUtils.small_body(c2)

            and

            CandleUtils.bullish(c3)

            and

            c3["Close"] > midpoint

        ):

            patterns.append(

                "Morning Star"

            )

            buy += 25

        # =====================================
        # Evening Star
        # =====================================

        midpoint = (

            c1["Open"] +

            c1["Close"]

        ) / 2

        if (

            CandleUtils.bullish(c1)

            and

            CandleUtils.small_body(c2)

            and

            CandleUtils.bearish(c3)

            and

            c3["Close"] < midpoint

        ):

            patterns.append(

                "Evening Star"

            )

            sell += 25

        # =====================================
        # Three White Soldiers
        # =====================================

        if (

            CandleUtils.bullish(c1)

            and

            CandleUtils.bullish(c2)

            and

            CandleUtils.bullish(c3)

            and

            c1["Close"] < c2["Close"] < c3["Close"]

        ):

            patterns.append(

                "Three White Soldiers"

            )

            buy += 30

        # =====================================
        # Three Black Crows
        # =====================================

        if (

            CandleUtils.bearish(c1)

            and

            CandleUtils.bearish(c2)

            and

            CandleUtils.bearish(c3)

            and

            c1["Close"] > c2["Close"] > c3["Close"]

        ):

            patterns.append(

                "Three Black Crows"

            )

            sell += 30

        # =====================================
        # Three Inside Up
        # =====================================

        if (

            CandleUtils.bearish(c1)

            and

            CandleUtils.bullish(c2)

            and

            CandleUtils.bullish(c3)

            and

            c3["Close"] > c1["Open"]

        ):

            patterns.append(

                "Three Inside Up"

            )

            buy += 18

        # =====================================
        # Three Inside Down
        # =====================================

        if (

            CandleUtils.bullish(c1)

            and

            CandleUtils.bearish(c2)

            and

            CandleUtils.bearish(c3)

            and

            c3["Close"] < c1["Open"]

        ):

            patterns.append(

                "Three Inside Down"

            )

            sell += 18

        # =====================================
        # Three Outside Up
        # =====================================

        if (

            CandleUtils.bearish(c1)

            and

            CandleUtils.bullish(c2)

            and

            CandleUtils.bullish(c3)

            and

            c2["Close"] > c1["Open"]

            and

            c3["Close"] > c2["Close"]

        ):

            patterns.append(

                "Three Outside Up"

            )

            buy += 20

        # =====================================
        # Three Outside Down
        # =====================================

        if (

            CandleUtils.bullish(c1)

            and

            CandleUtils.bearish(c2)

            and

            CandleUtils.bearish(c3)

            and

            c2["Close"] < c1["Open"]

            and

            c3["Close"] < c2["Close"]

        ):

            patterns.append(

                "Three Outside Down"

            )

            sell += 20

        return {

            "buy": buy,

            "sell": sell,

            "patterns": patterns

        }