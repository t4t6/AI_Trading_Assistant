import pandas as pd


class RiskManager:

    @staticmethod
    def calculate(df: pd.DataFrame, signal: str):

        row = df.iloc[-1]

        entry = float(row["Close"])
        atr = float(row["ATR"])

        swing_high = float(df["High"].tail(20).max())
        swing_low = float(df["Low"].tail(20).min())

        if atr <= 0:
            atr = entry * 0.005

        # =====================================================
        # BUY
        # =====================================================

        if signal in ["BUY", "STRONG BUY"]:

            stop_loss = min(

                swing_low,

                entry - (2.0 * atr)

            )

            risk = entry - stop_loss

            tp1 = entry + (risk * 1.0)

            tp2 = entry + (risk * 2.0)

            tp3 = entry + (risk * 3.0)

        # =====================================================
        # SELL
        # =====================================================

        elif signal in ["SELL", "STRONG SELL"]:

            stop_loss = max(

                swing_high,

                entry + (2.0 * atr)

            )

            risk = stop_loss - entry

            tp1 = entry - (risk * 1.0)

            tp2 = entry - (risk * 2.0)

            tp3 = entry - (risk * 3.0)

        # =====================================================
        # WAIT
        # =====================================================

        else:

            stop_loss = entry

            tp1 = entry

            tp2 = entry

            tp3 = entry

            risk = 0

        # =====================================================
        # Risk Reward
        # =====================================================

        if risk > 0:

            rr1 = round((tp1 - entry) / risk, 2)

            rr2 = round((tp2 - entry) / risk, 2)

            rr3 = round((tp3 - entry) / risk, 2)

        else:

            rr1 = 0

            rr2 = 0

            rr3 = 0

        return {

            "entry": round(entry, 5),

            "stop_loss": round(stop_loss, 5),

            "take_profit_1": round(tp1, 5),

            "take_profit_2": round(tp2, 5),

            "take_profit_3": round(tp3, 5),

            "risk": round(risk, 5),

            "risk_reward_1": rr1,

            "risk_reward_2": rr2,

            "risk_reward_3": rr3

        }