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

class EWMA(Strategy):
    """
    Estrategia de medias moviles exponenciales
    """
    n1 = 5
    n2 = 13

    # Definir parámetros
    def init(self):
        self.ewma1 = self.I(EWMA, self.data.Close, self.n1)
        self.ewma2 = self.I(EWMA, self.data.Close, self.n2)

    # Definir estrategia
    def next(self):
        if crossover(self.ewma1, self.ewma2):
            self.buy()
        elif crossover(self.ewma2, self.ewma1):
            self.position.close()

class BollingerBands(Strategy):
    """
    Estrategia de bandas de Bollinger
    """
    n1 = 20
    n2 = 2

    # Definir parámetros
    def init(self):
        self.bb = self.I(BollingerBands, self.data.Close, self.n1, self.n2)

    # Definir estrategia
    def next(self):
        if self.data.Close[-1] < self.bb.lowerband[-1]:
            self.buy()
        elif self.data.Close[-1] > self.bb.upperband[-1]:
            self.position.close()