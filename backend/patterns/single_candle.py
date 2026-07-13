from .candle_utils import CandleUtils


class SinglePatterns:

    @staticmethod
    def detect(df):

        c = df.iloc[-1]

        patterns = []

        buy = 0

        sell = 0

        if CandleUtils.doji(c):

            patterns.append("Doji")

        if CandleUtils.hammer(c):

            patterns.append("Hammer")

            buy += 8

        if CandleUtils.shooting_star(c):

            patterns.append("Shooting Star")

            sell += 8

        if CandleUtils.marubozu(c):

            if CandleUtils.bullish(c):

                patterns.append("Bullish Marubozu")

                buy += 10

            else:

                patterns.append("Bearish Marubozu")

                sell += 10

        return {

            "buy": buy,

            "sell": sell,

            "patterns": patterns

        }