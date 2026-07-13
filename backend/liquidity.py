import pandas as pd


class Liquidity:

    SWING = 5

    EQUAL_TOLERANCE = 0.0008

    SWEEP_TOLERANCE = 0.0015

    @staticmethod
    def analyze(df: pd.DataFrame):

        highs = df["High"].tolist()
        lows = df["Low"].tolist()
        closes = df["Close"].tolist()

        current_price = float(closes[-1])

        buy = 0
        sell = 0

        reasons = []

        equal_highs = []
        equal_lows = []

        buy_side = []
        sell_side = []

        # =========================================
        # Equal Highs
        # =========================================

        for i in range(len(highs) - 1):

            for j in range(i + 1, len(highs)):

                difference = abs(

                    highs[i] - highs[j]

                ) / highs[i]

                if difference <= Liquidity.EQUAL_TOLERANCE:

                    equal_highs.append({

                        "price": highs[i],

                        "first": i,

                        "second": j

                    })

        # =========================================
        # Equal Lows
        # =========================================

        for i in range(len(lows) - 1):

            for j in range(i + 1, len(lows)):

                difference = abs(

                    lows[i] - lows[j]

                ) / lows[i]

                if difference <= Liquidity.EQUAL_TOLERANCE:

                    equal_lows.append({

                        "price": lows[i],

                        "first": i,

                        "second": j

                    })

        # =========================================
        # Buy-side Liquidity
        # =========================================

        for level in equal_highs:

            if level["price"] > current_price:

                buy_side.append(level)

        # =========================================
        # Sell-side Liquidity
        # =========================================

        for level in equal_lows:

            if level["price"] < current_price:

                sell_side.append(level)

        # =========================================
        # Liquidity Sweep Detection
        # =========================================

        bullish_sweep = False
        bearish_sweep = False

        latest_high = highs[-1]
        latest_low = lows[-1]
        latest_close = closes[-1]

        for level in buy_side:

            if latest_high > level["price"]:

                if latest_close < level["price"]:

                    bearish_sweep = True

                    sell += 20

                    reasons.append(

                        "Buy-side Liquidity Sweep"

                    )

                    break

        for level in sell_side:

            if latest_low < level["price"]:

                if latest_close > level["price"]:

                    bullish_sweep = True

                    buy += 20

                    reasons.append(

                        "Sell-side Liquidity Sweep"

                    )

                    break

        # =========================================
        # Near Liquidity Pool
        # =========================================

        nearest_buy = None
        nearest_sell = None

        buy_distance = 999999999
        sell_distance = 999999999

        for level in buy_side:

            distance = abs(

                level["price"] -

                current_price

            )

            if distance < buy_distance:

                buy_distance = distance

                nearest_buy = level

        for level in sell_side:

            distance = abs(

                level["price"] -

                current_price

            )

            if distance < sell_distance:

                sell_distance = distance

                nearest_sell = level

        if nearest_buy:

            if (

                buy_distance /

                current_price

            ) < 0.002:

                sell += 8

                reasons.append(

                    "Price Near Buy-side Liquidity"

                )

        if nearest_sell:

            if (

                sell_distance /

                current_price

            ) < 0.002:

                buy += 8

                reasons.append(

                    "Price Near Sell-side Liquidity"

                )

        return {

            "buy": buy,

            "sell": sell,

            "bullish_sweep": bullish_sweep,

            "bearish_sweep": bearish_sweep,

            "equal_highs": equal_highs,

            "equal_lows": equal_lows,

            "buy_side_liquidity": buy_side,

            "sell_side_liquidity": sell_side,

            "nearest_buy_liquidity": nearest_buy,

            "nearest_sell_liquidity": nearest_sell,

            "reasons": reasons

        }