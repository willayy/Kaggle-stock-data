"""This module is responsible for loading the dataset from Kaggle."""

import kagglehub as khub
import pandas as pd
from pandas import DataFrame

DL_REF: str = "jacksoncrow/stock-market-dataset"


def load_dataset(asset: str, ticker: str) -> DataFrame:
    """Load the dataset from Kaggle.
    type is either 'stocks' or 'etfs'.
    Ticker is the stock or ETF symbol.
    For example, 'AAPL' for Apple."""

    path = khub.dataset_download(DL_REF)
    path += f"/{asset}/{ticker}.csv"
    df = pd.read_csv(path)
    return df
