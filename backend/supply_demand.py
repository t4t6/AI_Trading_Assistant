import pandas as pd


class SupplyDemand:

    BASE_CANDLES = 3

    IMPULSE_FACTOR = 1.8

    @staticmethod
    def analyze(df: pd.DataFrame):

        zones = []

        atr = float(df.iloc[-1]["ATR"])

        closes = df["Close"].tolist()
        highs = df["High"].tolist()
        lows = df["Low"].tolist()
        opens = df["Open"].tolist()

        # ==========================================
        # Demand Zones
        # ==========================================

        for i in range(10, len(df) - 5):

            base_high = max(

                highs[i:i + SupplyDemand.BASE_CANDLES]

            )

            base_low = min(

                lows[i:i + SupplyDemand.BASE_CANDLES]

            )

            move = (

                closes[i + 3] -

                closes[i]

            )

            if move > atr * SupplyDemand.IMPULSE_FACTOR:

                zones.append({

                    "type": "DEMAND",

                    "high": base_high,

                    "low": base_low,

                    "created": i

                })

        # ==========================================
        # Supply Zones
        # ==========================================

        for i in range(10, len(df) - 5):

            base_high = max(

                highs[i:i + SupplyDemand.BASE_CANDLES]

            )

            base_low = min(

                lows[i:i + SupplyDemand.BASE_CANDLES]

            )

            move = (

                closes[i] -

                closes[i + 3]

            )

            if move > atr * SupplyDemand.IMPULSE_FACTOR:

                zones.append({

                    "type": "SUPPLY",

                    "high": base_high,

                    "low": base_low,

                    "created": i

                })

        price = float(df.iloc[-1]["Close"])

        nearest_supply = None
        nearest_demand = None

        for zone in zones:

            if zone["type"] == "SUPPLY":

                if zone["low"] >= price:

                    if (

                        nearest_supply is None or

                        zone["low"] < nearest_supply["low"]

                    ):

                        nearest_supply = zone

            if zone["type"] == "DEMAND":

                if zone["high"] <= price:

                    if (

                        nearest_demand is None or

                        zone["high"] > nearest_demand["high"]

                    ):

                        nearest_demand = zone

        buy = 0
        sell = 0

        reasons = []

        # ==========================================
        # Demand
        # ==========================================

        if nearest_demand:

            distance = (

                price -

                nearest_demand["high"]

            ) / price

            if distance < 0.003:

                buy += 15

                reasons.append(

                    "Price Inside Demand Zone"

                )

        # ==========================================
        # Supply
        # ==========================================

        if nearest_supply:

            distance = (

                nearest_supply["low"] -

                price

            ) / price

            if distance < 0.003:

                sell += 15

                reasons.append(

                    "Price Inside Supply Zone"

                )

        return {

            "buy": buy,

            "sell": sell,

            "zones": zones,

            "nearest_supply": nearest_supply,

            "nearest_demand": nearest_demand,

            "reasons": reasons

        }