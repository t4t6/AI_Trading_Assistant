import pandas as pd


class CandleUtils:

    @staticmethod
    def body(c):

        return abs(

            c["Close"] -

            c["Open"]

        )

    @staticmethod
    def range(c):

        return (

            c["High"] -

            c["Low"]

        )

    @staticmethod
    def upper_wick(c):

        return (

            c["High"] -

            max(

                c["Open"],

                c["Close"]

            )

        )

    @staticmethod
    def lower_wick(c):

        return (

            min(

                c["Open"],

                c["Close"]

            ) -

            c["Low"]

        )

    @staticmethod
    def bullish(c):

        return c["Close"] > c["Open"]

    @staticmethod
    def bearish(c):

        return c["Close"] < c["Open"]

    @staticmethod
    def small_body(c):

        return (

            CandleUtils.body(c)

            <

            CandleUtils.range(c) * 0.30

        )

    @staticmethod
    def long_body(c):

        return (

            CandleUtils.body(c)

            >

            CandleUtils.range(c) * 0.70

        )

    @staticmethod
    def doji(c):

        return (

            CandleUtils.body(c)

            <=

            CandleUtils.range(c) * 0.10

        )

    @staticmethod
    def hammer(c):

        return (

            CandleUtils.lower_wick(c)

            >

            CandleUtils.body(c) * 2

            and

            CandleUtils.upper_wick(c)

            <

            CandleUtils.body(c)

        )

    @staticmethod
    def shooting_star(c):

        return (

            CandleUtils.upper_wick(c)

            >

            CandleUtils.body(c) * 2

            and

            CandleUtils.lower_wick(c)

            <

            CandleUtils.body(c)

        )

    @staticmethod
    def marubozu(c):

        return (

            CandleUtils.upper_wick(c)

            <

            CandleUtils.range(c) * 0.05

            and

            CandleUtils.lower_wick(c)

            <

            CandleUtils.range(c) * 0.05

        )