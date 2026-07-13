from .single_candle import SinglePatterns
from .double_candle import DoublePatterns
from .triple_candle import TriplePatterns


class PatternEngine:

    @staticmethod
    def analyze(df):

        single = SinglePatterns.detect(df)

        double = DoublePatterns.detect(df)

        triple = TriplePatterns.detect(df)

        buy = (

            single["buy"] +

            double["buy"] +

            triple["buy"]

        )

        sell = (

            single["sell"] +

            double["sell"] +

            triple["sell"]

        )

        patterns = []

        patterns.extend(

            single["patterns"]

        )

        patterns.extend(

            double["patterns"]

        )

        patterns.extend(

            triple["patterns"]

        )

        strength = abs(

            buy -

            sell

        )

        if strength >= 50:

            quality = "VERY STRONG"

        elif strength >= 35:

            quality = "STRONG"

        elif strength >= 20:

            quality = "MEDIUM"

        elif strength >= 10:

            quality = "WEAK"

        else:

            quality = "NEUTRAL"

        dominant = "NEUTRAL"

        if buy > sell:

            dominant = "BULLISH"

        elif sell > buy:

            dominant = "BEARISH"

        return {

            "buy": buy,

            "sell": sell,

            "patterns": patterns,

            "pattern_count": len(patterns),

            "dominant": dominant,

            "quality": quality,

            "strength": strength

        }