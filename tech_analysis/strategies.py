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

class EWMA(Strategy):
    """
    Exponential Moving Average (EWMA) Crossover Strategy.
    Inherits from the Strategy base class.
    
    - Buys when the fast EWMA crosses above the slow EWMA.
    - Closes the position when the fast EWMA crosses below the slow EWMA.

    """
    n1 = 5
    n2 = 13

    # Define parameters
    def init(self):
        self.ewma1 = self.I(EWMA, self.data.Close, self.n1)
        self.ewma2 = self.I(EWMA, self.data.Close, self.n2)

    # Define strategy
    def next(self):
        if crossover(self.ewma1, self.ewma2):
            self.buy()
        elif crossover(self.ewma2, self.ewma1):
            self.position.close()

class BollingerBands(Strategy):
    """
    Bollinger Bands Strategy.
    Inherits from the Strategy base class.
    
    - Buys when the price closes below the lower Bollinger Band.
    - Closes the position when the price closes above the upper Bollinger Band.

    """
    n1 = 20
    n2 = 2

    # Define parameters
    def init(self):
        self.bb = self.I(BollingerBands, self.data.Close, self.n1, self.n2)

    # Define strategy
    def next(self):
        if self.data.Close[-1] < self.bb.lowerband[-1]:
            self.buy()
        elif self.data.Close[-1] > self.bb.upperband[-1]:
            self.position.close()