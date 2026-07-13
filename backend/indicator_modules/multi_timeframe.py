from market_data import MarketData
from indicators import IndicatorEngine


class MultiTimeframeAnalyzer:

    TIMEFRAMES = [

        "1m",
        "2m",
        "5m",
        "15m",
        "30m",
        "1h",
        "4h",
        "1d"

    ]

    @staticmethod
    def _trend(df):

        row = df.iloc[-1]

        score = 0

        # EMA Trend

        if row["EMA_9"] > row["EMA_21"] > row["EMA_50"]:

            score += 1

        elif row["EMA_9"] < row["EMA_21"] < row["EMA_50"]:

            score -= 1

        # MACD

        if row["MACD"] > row["MACD_SIGNAL"]:

            score += 1

        else:

            score -= 1

        # RSI

        if row["RSI"] >= 55:

            score += 1

        elif row["RSI"] <= 45:

            score -= 1

        # ADX Direction

        if row["ADX"] >= 25:

            if row["DI_PLUS"] > row["DI_MINUS"]:

                score += 1

            else:

                score -= 1

        return score

    @staticmethod
    def analyze(symbol):

        buy = 0

        sell = 0

        bullish = 0

        bearish = 0

        details = []

        for tf in MultiTimeframeAnalyzer.TIMEFRAMES:

            try:

                df = MarketData.get_data(

                    symbol=symbol,

                    interval=tf

                )

                if df.empty:

                    continue

                df = IndicatorEngine.calculate(df)

                score = MultiTimeframeAnalyzer._trend(df)

                if score > 0:

                    bullish += 1

                    buy += score

                    details.append({

                        "timeframe": tf,

                        "trend": "BULLISH"

                    })

                elif score < 0:

                    bearish += 1

                    sell += abs(score)

                    details.append({

                        "timeframe": tf,

                        "trend": "BEARISH"

                    })

                else:

                    details.append({

                        "timeframe": tf,

                        "trend": "NEUTRAL"

                    })

            except Exception:

                continue

        total = bullish + bearish

        if total == 0:

            alignment = 0

        else:

            alignment = round(

                max(bullish, bearish) / total * 100

            )

        if bullish > bearish:

            overall = "BULLISH"

        elif bearish > bullish:

            overall = "BEARISH"

        else:

            overall = "MIXED"

        return {

            "buy": buy,

            "sell": sell,

            "bullish": bullish,

            "bearish": bearish,

            "alignment": alignment,

            "overall": overall,

            "details": details

        }