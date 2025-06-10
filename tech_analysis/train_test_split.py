import yfinance as yf

class TrainTestSets:

    def __init__(self):
        pass

    def train_test_split(self, ticker, interval):
        """_summary_

        Args:
            ticker (_type_): _description_
            interval (_type_): _description_

        Returns:
            _type_: _description_
        """

        if interval in ["1m", "2m", "5m", "30m"]:
            start = "2025-05-31"
            end = "2025-06-06"
        elif interval in ["15m", "60m", "90m"]:
            start = "2025-04-28"
            end = "2025-06-06"
        elif interval in ["1h", "4h", "1d", "5d", "1wk"]:
            start = "2024-06-06"
            end = "2025-06-06"
        data = yf.download(tickers = ticker, start=start, end=end, interval=interval)
        data.columns = data.columns.droplevel(1)
        # Calculamos el punto de corte
        split_idx = int(len(data)*0.7)
        # Particiones respetando la secuencia temporal
        train = data.iloc[:split_idx]
        test = data.iloc[split_idx:]
        return (train, test)
    
    def interval_train_test_split(self, ticker, intervals):
        all_data = {}

        for interval in intervals:
            data_from_split = train_test_split(self, ticker, interval)
            all_data[f"{interval}_train"] = data_from_split[0]
            all_data[f"{interval}_test"] = data_from_split[1]

        return all_data