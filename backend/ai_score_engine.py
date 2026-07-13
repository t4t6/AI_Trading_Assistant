from market_structure import MarketStructure
from support_resistance import SupportResistance
from supply_demand import SupplyDemand
from fair_value_gap import FairValueGap
from liquidity import Liquidity
from order_blocks import OrderBlocks

from patterns import PatternEngine


class AIScoreEngine:

    @staticmethod
    def calculate(df):

        # =====================================
        # Run Every AI Module
        # =====================================

        structure = MarketStructure.analyze(df)

        sr = SupportResistance.analyze(df)

        sd = SupplyDemand.analyze(df)

        fvg = FairValueGap.analyze(df)

        liquidity = Liquidity.analyze(df)

        orderblocks = OrderBlocks.analyze(df)

        patterns = PatternEngine.analyze(df)

        # =====================================
        # Buy/Sell Score
        # =====================================

        buy = 0

        sell = 0

        reasons = []

        modules = [

            sr,

            sd,

            fvg,

            liquidity,

            orderblocks,

            patterns

        ]

        for module in modules:

            buy += module["buy"]

            sell += module["sell"]

            reasons.extend(

                module.get(

                    "reasons",

                    []

                )

            )

        # =====================================
        # Market Structure
        # =====================================

        if structure["trend"] == "UPTREND":

            buy += 20

            reasons.append(

                "Higher Highs / Higher Lows"

            )

        elif structure["trend"] == "DOWNTREND":

            sell += 20

            reasons.append(

                "Lower Highs / Lower Lows"

            )

        if structure["bos"]:

            if structure["bos_direction"] == "BULLISH":

                buy += 15

                reasons.append(

                    "Bullish Break of Structure"

                )

            else:

                sell += 15

                reasons.append(

                    "Bearish Break of Structure"

                )

        if structure["choch"]:

            reasons.append(

                "Change Of Character"

            )

        # =====================================
        # Confidence
        # =====================================

        total = buy + sell

        if total == 0:

            confidence = 50

        else:

            confidence = round(

                max(

                    buy,

                    sell

                )

                /

                total

                *

                100,

                1

            )

        # =====================================
        # Final Signal
        # =====================================

        if buy >= sell + 40:

            signal = "STRONG BUY"

        elif buy > sell:

            signal = "BUY"

        elif sell >= buy + 40:

            signal = "STRONG SELL"

        elif sell > buy:

            signal = "SELL"

        else:

            signal = "WAIT"

        # =====================================
        # Binary Direction
        # =====================================

        if buy > sell:

            binary = "BULLISH"

        elif sell > buy:

            binary = "BEARISH"

        else:

            binary = "NEUTRAL"

        # =====================================
        # Trade Quality
        # =====================================

        difference = abs(

            buy - sell

        )

        if difference >= 80:

            stars = 5

        elif difference >= 60:

            stars = 4

        elif difference >= 40:

            stars = 3

        elif difference >= 20:

            stars = 2

        else:

            stars = 1

        return {

            "buy_score": buy,

            "sell_score": sell,

            "confidence": confidence,

            "signal": signal,

            "binary": binary,

            "trade_quality": stars,

            "market_structure": structure,

            "support_resistance": sr,

            "supply_demand": sd,

            "fair_value_gap": fvg,

            "liquidity": liquidity,

            "order_blocks": orderblocks,

            "patterns": patterns,

            "reasons": reasons

        }