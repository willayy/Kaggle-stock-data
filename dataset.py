import kagglehub as khub
import pandas as pd
from pandas import DataFrame

DL_REF = 'jacksoncrow/stock-market-dataset'

def load_dataset(type: str, ticker: str) -> DataFrame:
    path = khub.dataset_download(DL_REF)
    path += f'/{type}/{ticker}.csv'
    df = pd.read_csv(path)
    return df