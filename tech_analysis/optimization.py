from backtesting import Backtest
import pandas as pd
import warnings
warnings.simplefilter('ignore')

class SMAOptTechAnalysis:

    def __init__(self, Strategy):
        self.strategy = Strategy
        pass

    def sma_params_n_tf_optimization(self, set_type, data, n1, n2, param = 'Return [%]'):
        bt = Backtest(data, self.strategy, cash=10_000_000, commission=0.002)
        stats, heatmap = bt.optimize(
        # Óptimos parámetros a optimizar
        n1= n1,
        n2= n2,
        constraint = lambda p : p.n1 < p.n2, # Restricciones
        maximize= param, # Aquí podemos usar las métricas de rendimiento de stats
        return_heatmap=True # Mapa de calor
        )

        best_params = heatmap.sort_values(ascending=False)

        best_results = {'interval': set_type, 'n1': best_params.index[0][0], 'n2': best_params.index[0][1], 'Return [%]': best_params.iloc[0], 'No. of Trades': stats['# Trades']}

        return best_results
    
    def sma_strategy_optimization(self, all_data, n1, n2):
        train_results = []
        for set_type, df in all_data.items():
            if "train" in set_type:
                train_results.append(self.sma_params_n_tf_optimization(set_type, df, n1, n2))

        optimal_tf_df = pd.DataFrame(train_results)
        return optimal_tf_df.sort_values(by='Return [%]', ascending=False)
