import streamlit as st
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.test import SMA, GOOG
# df = st.session_state.returns.copy()


# def test_strat(data,init_balance):
#     df = data.copy()


import pandas as pd
def EMA(arr: pd.Series, n: int) -> pd.Series:
    """
    Returns `n`-period simple moving average of array `arr`.
    """
    return pd.Series(arr).ewm(span=n).mean()

# out['close'].ewm(span=20).mean()

class EmaCross(Strategy):
    n1=20
    n2=50
    def init(self):
        price = self.data.Close
        self.ema1 = self.I(EMA, price, 20)
        self.ema2 = self.I(EMA, price, 50)

    def next(self):
        if crossover(self.ema1, self.ema2):
            self.buy()
        elif crossover(self.ema2, self.ema1):
            self.sell()