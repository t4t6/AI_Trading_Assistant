import pandas as pd

from ta.trend import EMAIndicator
from ta.trend import SMAIndicator
from ta.trend import MACD
from ta.trend import ADXIndicator
from ta.trend import CCIIndicator
from ta.trend import IchimokuIndicator
from ta.trend import PSARIndicator

from ta.momentum import RSIIndicator
from ta.momentum import StochasticOscillator
from ta.momentum import StochRSIIndicator
from ta.momentum import WilliamsRIndicator
from ta.momentum import ROCIndicator

from ta.volatility import BollingerBands
from ta.volatility import AverageTrueRange
from ta.volatility import DonchianChannel
from ta.volatility import KeltnerChannel

from ta.volume import OnBalanceVolumeIndicator
from ta.volume import MFIIndicator


class IndicatorEngine:

    @staticmethod
    def calculate(df: pd.DataFrame):

        data = df.copy()

        # ===========================
        # EMA
        # ===========================

        data["EMA_9"] = EMAIndicator(
            close=data["Close"],
            window=9
        ).ema_indicator()

        data["EMA_21"] = EMAIndicator(
            close=data["Close"],
            window=21
        ).ema_indicator()

        data["EMA_50"] = EMAIndicator(
            close=data["Close"],
            window=50
        ).ema_indicator()

        data["EMA_100"] = EMAIndicator(
            close=data["Close"],
            window=100
        ).ema_indicator()

        data["EMA_200"] = EMAIndicator(
            close=data["Close"],
            window=200
        ).ema_indicator()

        # ===========================
        # SMA
        # ===========================

        data["SMA_20"] = SMAIndicator(
            close=data["Close"],
            window=20
        ).sma_indicator()

        data["SMA_50"] = SMAIndicator(
            close=data["Close"],
            window=50
        ).sma_indicator()

        data["SMA_200"] = SMAIndicator(
            close=data["Close"],
            window=200
        ).sma_indicator()

        # ===========================
        # RSI
        # ===========================

        data["RSI"] = RSIIndicator(
            close=data["Close"]
        ).rsi()

        # ===========================
        # MACD
        # ===========================

        macd = MACD(close=data["Close"])

        data["MACD"] = macd.macd()

        data["MACD_SIGNAL"] = macd.macd_signal()

        data["MACD_HIST"] = macd.macd_diff()

        # ===========================
        # ADX
        # ===========================

        adx = ADXIndicator(

            high=data["High"],

            low=data["Low"],

            close=data["Close"]

        )

        data["ADX"] = adx.adx()

        data["DI_PLUS"] = adx.adx_pos()

        data["DI_MINUS"] = adx.adx_neg()

        # ===========================
        # STOCHASTIC
        # ===========================

        stoch = StochasticOscillator(

            high=data["High"],

            low=data["Low"],

            close=data["Close"]

        )

        data["STOCH_K"] = stoch.stoch()

        data["STOCH_D"] = stoch.stoch_signal()

        # ===========================
        # STOCH RSI
        # ===========================

        srsi = StochRSIIndicator(
            close=data["Close"]
        )

        data["STOCH_RSI"] = srsi.stochrsi()

        # ===========================
        # CCI
        # ===========================

        cci = CCIIndicator(

            high=data["High"],

            low=data["Low"],

            close=data["Close"]

        )

        data["CCI"] = cci.cci()

        # ===========================
        # WILLIAMS %R
        # ===========================

        wr = WilliamsRIndicator(

            high=data["High"],

            low=data["Low"],

            close=data["Close"]

        )

        data["WILLIAMS_R"] = wr.williams_r()

        # ===========================
        # ROC
        # ===========================

        roc = ROCIndicator(
            close=data["Close"]
        )

        data["ROC"] = roc.roc()

        # ===========================
        # ATR
        # ===========================

        atr = AverageTrueRange(

            high=data["High"],

            low=data["Low"],

            close=data["Close"]

        )

        data["ATR"] = atr.average_true_range()

        # ===========================
        # BOLLINGER
        # ===========================

        bb = BollingerBands(
            close=data["Close"]
        )

        data["BB_UPPER"] = bb.bollinger_hband()

        data["BB_MIDDLE"] = bb.bollinger_mavg()

        data["BB_LOWER"] = bb.bollinger_lband()

        # ===========================
        # DONCHIAN
        # ===========================

        dc = DonchianChannel(

            high=data["High"],

            low=data["Low"],

            close=data["Close"]

        )

        data["DONCHIAN_HIGH"] = dc.donchian_channel_hband()

        data["DONCHIAN_LOW"] = dc.donchian_channel_lband()

        # ===========================
        # KELTNER
        # ===========================

        kc = KeltnerChannel(

            high=data["High"],

            low=data["Low"],

            close=data["Close"]

        )

        data["KC_UPPER"] = kc.keltner_channel_hband()

        data["KC_MIDDLE"] = kc.keltner_channel_mband()

        data["KC_LOWER"] = kc.keltner_channel_lband()

        # ===========================
        # OBV
        # ===========================

        obv = OnBalanceVolumeIndicator(

            close=data["Close"],

            volume=data["Volume"]

        )

        data["OBV"] = obv.on_balance_volume()

        # ===========================
        # MFI
        # ===========================

        mfi = MFIIndicator(

            high=data["High"],

            low=data["Low"],

            close=data["Close"],

            volume=data["Volume"]

        )

        data["MFI"] = mfi.money_flow_index()

        # ===========================
        # PSAR
        # ===========================

        psar = PSARIndicator(

            high=data["High"],

            low=data["Low"],

            close=data["Close"]

        )

        data["PSAR"] = psar.psar()

        # ===========================
        # ICHIMOKU
        # ===========================

        ichi = IchimokuIndicator(

            high=data["High"],

            low=data["Low"]

        )

        data["ICHI_CONVERSION"] = ichi.ichimoku_conversion_line()

        data["ICHI_BASE"] = ichi.ichimoku_base_line()

        data["ICHI_A"] = ichi.ichimoku_a()

        data["ICHI_B"] = ichi.ichimoku_b()

        return data