import pandas as pd

from market_data import MarketData
from indicators import IndicatorEngine
from ai_score_engine import AIScoreEngine

MTF_FRAMES = ["5m", "15m", "1h", "4h", "1d"]


class SignalEngine:

    # ============================================
    # Download + Indicator Data
    # ============================================

    @staticmethod
    def download(symbol, timeframe):
        df = MarketData.get_data(symbol, timeframe)

        if df is None or len(df) < 30:
            return None

        return df

    # ============================================
    # ATR Based Targets
    # ============================================

    @staticmethod
    def build_trade(df, signal):
        close = float(df.iloc[-1]["Close"])
        atr = float(df.iloc[-1]["ATR"]) if pd.notna(df.iloc[-1]["ATR"]) else 0

        if atr <= 0:
            atr = max(close * 0.005, 0.0001)

        volatility = atr / close

        if volatility >= 0.03:
            sl_multiplier, tp1_multiplier, tp2_multiplier, tp3_multiplier = 2.2, 2.5, 4.5, 7.0
        elif volatility >= 0.02:
            sl_multiplier, tp1_multiplier, tp2_multiplier, tp3_multiplier = 2.0, 2.2, 4.0, 6.0
        elif volatility >= 0.01:
            sl_multiplier, tp1_multiplier, tp2_multiplier, tp3_multiplier = 1.8, 2.0, 3.5, 5.5
        else:
            sl_multiplier, tp1_multiplier, tp2_multiplier, tp3_multiplier = 1.5, 1.8, 3.0, 5.0

        if signal in ("BUY", "STRONG BUY"):
            entry = close
            stop = close - atr * sl_multiplier
            tp1 = close + atr * tp1_multiplier
            tp2 = close + atr * tp2_multiplier
            tp3 = close + atr * tp3_multiplier
        elif signal in ("SELL", "STRONG SELL"):
            entry = close
            stop = close + atr * sl_multiplier
            tp1 = close - atr * tp1_multiplier
            tp2 = close - atr * tp2_multiplier
            tp3 = close - atr * tp3_multiplier
        else:
            entry = stop = tp1 = tp2 = tp3 = close

        risk = abs(entry - stop)
        reward = abs(tp1 - entry)
        rr = round(reward / risk, 2) if risk > 0 else 0

        return {
            "entry": round(entry, 5),
            "stop_loss": round(stop, 5),
            "take_profit_1": round(tp1, 5),
            "take_profit_2": round(tp2, 5),
            "take_profit_3": round(tp3, 5),
            "risk_reward": rr,
            "atr": round(atr, 5),
            "volatility_percent": round(volatility * 100, 2),
        }

    # ============================================
    # Volume Strength
    # ============================================

    @staticmethod
    def volume_strength(df):
        if "Volume" not in df.columns or len(df) < 20:
            return "N/A"

        recent = df["Volume"].tail(20)
        avg = recent.mean()
        current = df.iloc[-1]["Volume"]

        if avg <= 0:
            return "N/A"

        ratio = current / avg

        if ratio >= 1.8:
            return "VERY HIGH"
        elif ratio >= 1.3:
            return "HIGH"
        elif ratio >= 0.7:
            return "NORMAL"
        else:
            return "LOW"

    # ============================================
    # Multi Timeframe Confirmation
    # ============================================

    @staticmethod
    def timeframe_alignment(symbol):
        bullish = 0
        bearish = 0
        total = 0

        for tf in MTF_FRAMES:
            try:
                df = SignalEngine.download(symbol, tf)
                if df is None:
                    continue

                df = IndicatorEngine.calculate(df)
                result = AIScoreEngine.calculate(df)

                total += 1

                if result["binary"] == "BULLISH":
                    bullish += 1
                elif result["binary"] == "BEARISH":
                    bearish += 1
            except Exception:
                pass

        if total == 0:
            return 0

        return round(max(bullish, bearish) / total * 100)

    # ============================================
    # Generate Signal
    # ============================================

    @staticmethod
    def generate(symbol, timeframe, include_alignment=True):
        df = SignalEngine.download(symbol, timeframe)

        if df is None:
            return {
                "status": False,
                "symbol": symbol,
                "timeframe": timeframe,
                "message": "No data returned for this symbol/timeframe.",
            }

        df = IndicatorEngine.calculate(df)
        ai = AIScoreEngine.calculate(df)
        trade = SignalEngine.build_trade(df, ai["signal"])
        alignment = SignalEngine.timeframe_alignment(symbol) if include_alignment else None

        return {
            "status": True,
            "symbol": symbol,
            "timeframe": timeframe,
            "signal": ai["signal"],
            "confidence": ai["confidence"],
            "entry": trade["entry"],
            "stop_loss": trade["stop_loss"],
            "take_profit_1": trade["take_profit_1"],
            "take_profit_2": trade["take_profit_2"],
            "take_profit_3": trade["take_profit_3"],
            "risk_reward": trade["risk_reward"],
            "next_candle": ai["binary"],
            "trend": ai["market_structure"]["trend"],
            "trade_quality": ai["trade_quality"],
            "timeframe_alignment": alignment,
            "buy_score": ai["buy_score"],
            "sell_score": ai["sell_score"],
            "volatility": trade["volatility_percent"],
            "volume_strength": SignalEngine.volume_strength(df),
            "reasons": ai["reasons"][:8],
        }

    # ============================================
    # Binary (Next Candle) Signal — lighter weight
    # ============================================

    @staticmethod
    def generate_binary(symbol, timeframe):
        df = SignalEngine.download(symbol, timeframe)

        if df is None:
            return {
                "status": False,
                "symbol": symbol,
                "timeframe": timeframe,
                "message": "No data returned for this symbol/timeframe.",
            }

        df = IndicatorEngine.calculate(df)
        ai = AIScoreEngine.calculate(df)
        close = float(df.iloc[-1]["Close"])

        return {
            "status": True,
            "symbol": symbol,
            "timeframe": timeframe,
            "prediction": ai["binary"],
            "confidence": ai["confidence"],
            "current_price": round(close, 5),
            "trade_quality": ai["trade_quality"],
            "reasons": ai["reasons"][:5],
        }
