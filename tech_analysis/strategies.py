import pandas as pd
import numpy as np
from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
import warnings
warnings.simplefilter('ignore')

class SmaCross(Strategy):
    """
    Simple Moving Average (SMA) Crossover Strategy.
    Inherits from the Strategy base class.
    
    - Buys when the short-term SMA crosses above the long-term SMA.
    - Closes the position when the short-term SMA crosses below the long-term SMA.

    """
    n1 = 5
    n2 = 13

    # Define parameters
    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, self.n1)
        self.sma2 = self.I(SMA, self.data.Close, self.n2)

    # Define strategy
    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.position.close()

# Function to calculate Exponentially Weighted Moving Average (EWMA) as they are not available in backtesting library
def EWMA_func(array, span):
    series = pd.Series(array)
    return series.ewm(span=span, adjust=False).mean().values

class EWMA(Strategy):
    """
    Exponential Moving Average (EWMA) Crossover Strategy.
    Inherits from the Strategy base class.

    This strategy buys when a short-term EWMA crosses above a long-term EWMA,
    and closes the position when the short-term EWMA crosses below the long-term EWMA.
    """
    n1 = 5
    n2 = 13

    def init(self):
        self.ewma1 = self.I(EWMA_func, self.data.Close, self.n1)
        self.ewma2 = self.I(EWMA_func, self.data.Close, self.n2)

    def next(self):
        if crossover(self.ewma1, self.ewma2):
            self.buy()
        elif crossover(self.ewma2, self.ewma1):
            self.position.close()

# Function to calculate Bollinger Bands as they are not available in backtesting library
def bollinger_bands_func(array, window, num_std):
    series = pd.Series(array)  # Convertir a Series para poder usar rolling()
    rolling_mean = series.rolling(window=window).mean()
    rolling_std = series.rolling(window=window).std()

    upper_band = rolling_mean + (num_std * rolling_std)
    lower_band = rolling_mean - (num_std * rolling_std)

    return np.array([upper_band, lower_band])

class BollingerBands(Strategy):
    """
    Bollinger Bands Strategy.

    This strategy buys when the price closes below the lower band,
    and exits when the price closes above the upper band.
    """
    n1 = 20  # window
    n2 = 2   # number of standard deviations

    def init(self):
        self.upperband, self.lowerband = self.I(bollinger_bands_func, self.data.Close, self.n1, self.n2)

    def next(self):
        if self.data.Close[-1] < self.lowerband[-1]:
            self.buy()
        elif self.data.Close[-1] > self.upperband[-1]:
            self.position.close()