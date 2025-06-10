from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
import warnings
warnings.simplefilter('ignore')

class SmaCross(Strategy):
    """
    Estrategia de medias moviles simples
    """
    n1 = 5
    n2 = 13

    # Definir parámetros
    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, self.n1)
        self.sma2 = self.I(SMA, self.data.Close, self.n2)

    # Definir estrategia
    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.position.close()

#class Startegy2(Strategy):