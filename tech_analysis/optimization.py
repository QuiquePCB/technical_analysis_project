from backtesting import Backtest
import pandas as pd
import warnings
warnings.simplefilter('ignore')

class SMAOptTechAnalysis:

    def __init__(self, Strategy):
        self.strategy = Strategy
        pass

    def sma_params_n_tf_optimization(self, set_type:str, data:pd.DataFrame, n1:range , n2:range, param:str = 'Return [%]') -> dict:
        # Initialize backtest with given strategy, capital, and commission

        bt = Backtest(data, self.strategy, cash=10_000_000, commission=0.002)
        stats, heatmap = bt.optimize(
        # Optimize over n1 and n2 with a constraint and specified metric
        n1= n1,
        n2= n2,
        constraint = lambda p : p.n1 < p.n2, # Restrictions 
        maximize= param, # Metric to maximize
        return_heatmap=True # Return heatmap of results
        )

        # Sort heatmap to find best parameters
        best_params = heatmap.sort_values(ascending=False)

        best_results = {'interval': set_type, 'n1': best_params.index[0][0], 'n2': best_params.index[0][1], 'Return [%]': best_params.iloc[0], 'No. of Trades': stats['# Trades']}

        return best_results
    
    def sma_strategy_optimization(self, all_data:dict[str, pd.DataFrame], n1:range, n2:range) -> pd.DataFrame:
        # Iterate over all datasets and apply optimization
        train_results = []
        for set_type, df in all_data.items():
            if "train" in set_type:
                train_results.append(self.sma_params_n_tf_optimization(set_type, df, n1, n2))

        # Compile and return results sorted by performance
        optimal_tf_df = pd.DataFrame(train_results)
        return optimal_tf_df.sort_values(by='Return [%]', ascending=False)
    
class EWMAOptTechAnalysis:
    # Optimizes an Exponentially Weighted Moving Average (EWMA)-based trading strategy across training datasets and parameter ranges.
    def __init__(self, Strategy):
        self.strategy = Strategy
        pass
    
    def ewma_params_n_tf_optimization(self, set_type: str, data: pd.DataFrame, n1: range, n2: range, param: str = 'Return [%]') -> dict:
        bt = Backtest(data, self.strategy, cash=10_000_000, commission=0.002)
        stats, heatmap = bt.optimize(
    
        n1= n1,
        n2= n2,
        constraint = lambda p : p.n1 < p.n2, 
        maximize= param, 
        return_heatmap=True 
        )

        best_params = heatmap.sort_values(ascending=False)

        best_results = {'interval': set_type, 'n1': best_params.index[0][0], 'n2': best_params.index[0][1], 'Return [%]': best_params.iloc[0], 'No. of Trades': stats['# Trades']}

        return best_results
    
    def ewma_strategy_optimization(self, all_data: dict[str, pd.DataFrame], n1: range, n2: range) -> pd.DataFrame:
        train_results = []
        for set_type, df in all_data.items():
            if "train" in set_type:
                train_results.append(self.ewma_params_n_tf_optimization(set_type, df, n1, n2))

        optimal_tf_df = pd.DataFrame(train_results)
        return optimal_tf_df.sort_values(by='Return [%]', ascending=False)
    
class BollingerBandsOptTechAnalysis:
    # Performs optimization of a Bollinger Bands-based trading strategy over different training datasets and parameter configurations.
    def __init__(self, Strategy):
        self.strategy = Strategy
        pass
    
    def BollingerBands_params_n_tf_optimization(self, set_type: str, data: pd.DataFrame, n1_range: range, n2_range: range, param: str = 'Return [%]') -> dict:
        bt = Backtest(data, self.strategy,
                      cash=10_000_000, commission=0.002)
        stats, heatmap = bt.optimize(
            n1 = n1_range,
            n2 = n2_range,
            constraint = lambda p: (p.n1 > 1) and (p.n2 > 0),
            maximize = param,
            return_heatmap = True,
        )

        best_params = heatmap.sort_values(ascending=False).iloc[0]
        
        best_results = {'interval': set_type, 'n1': best_params.index[0][0], 'n2': best_params.index[0][1], 'Return [%]': best_params.iloc[0], 'No. of Trades': stats['# Trades']}

        return best_results

    def bollinger_strategy_optimization(self, all_data: dict[str, pd.DataFrame], n1_range: range, n2_range: range) -> pd.DataFrame:
        results = []
        for set_type, df in all_data.items():
            if "train" in set_type:
                res = self.BollingerBands_params_n_tf_optimization(
                    set_type, df, n1_range, n2_range
                )
                results.append(res)
        df_opt = pd.DataFrame(results)
        return df_opt.sort_values(by='Return [%]', ascending=False)