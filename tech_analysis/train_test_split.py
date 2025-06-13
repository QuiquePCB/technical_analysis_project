import yfinance as yf

class TrainTestSets:

    def __init__(self):
        pass

    def train_test_split(self, ticker, interval):

        """
        Download historical data for a given ticker and interval, and split it into
        chronological training and testing sets.

        Arguments:
            ticker:  symbol for the stock or asset to download data for
            interval: data interval accepted by yfinance.

        Returns:
            tuple: A tuple containing the training and testing datasets as pandas DataFrames.
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
        # Download data using yfinance
        data = yf.download(tickers = ticker, start=start, end=end, interval=interval)
        data.columns = data.columns.droplevel(1)
         # Calculate split index (70% train, 30% test)
        split_idx = int(len(data)*0.7)
        # Create train and test sets while preserving temporal order
        train = data.iloc[:split_idx]
        test = data.iloc[split_idx:]
        return (train, test)
    
    def interval_train_test_split(self, ticker, intervals):
        """
        Generate training and testing splits for multiple time intervals

        Args:
            ticker 
            intervals: List of time intervals

        Returns:
            dict: A dictionary where keys are labeled with the interval and train/test suffix,
                  and values are the corresponding pandas DataFrames.
        """
        all_data = {}

        for interval in intervals:
            data_from_split = self.train_test_split(ticker, interval)
            all_data[f"{interval}_train"] = data_from_split[0]
            all_data[f"{interval}_test"] = data_from_split[1]

        return all_data

