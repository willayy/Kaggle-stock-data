"""This module is responsible for loading the dataset from Kaggle."""

from datetime import timedelta
import matplotlib.dates as mdates
import kagglehub as khub
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame
import mplcursors

DL_REF: str = "jacksoncrow/stock-market-dataset"

def get_stock_data(asset: str, ticker: str) -> DataFrame:
    """Load the dataset from Kaggle.
    type is either 'stocks' or 'etfs'.
    Ticker is the stock or ETF symbol.
    For example, 'AAPL' for Apple."""

    path = khub.dataset_download(DL_REF)
    path += f"/{asset}/{ticker}.csv"
    df = pd.read_csv(path)
    return df


def display_stock_df(df: DataFrame) -> None:
    """Display the asset DataFrame as a candle stick chart with volume."""

    # Range
    volume_scale = 10_000_000
    start_row = 7000
    end_row = 7100
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date", ascending=True)
    df["Volume"] = df["Volume"] / volume_scale
    ranged_df = df.iloc[start_row:end_row]
    x_lim_start, x_lim_end = (ranged_df["Date"].min(), ranged_df["Date"].max())
    y_lim_start, y_lim_end = (
        ranged_df["Low"].min() * 0.9,
        ranged_df["High"].max() * 1.1,
    )

    _, ax = plt.subplots()
    ax.grid()
    ax.set_title("Candlestick Chart")
    ax.set_xlim(x_lim_start, x_lim_end)
    ax.set_ylim(y_lim_start, y_lim_end)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d:%H"))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.tick_params(axis="x", rotation=45, labelsize=10)

    # Candlestick
    ax.vlines(
        ranged_df["Date"],
        ranged_df["Low"],
        ranged_df["High"],
        color="black",
        linewidth=1,
    )
    ax.hlines(
        ranged_df["High"],
        ranged_df["Date"] - timedelta(hours=12),
        ranged_df["Date"] + timedelta(hours=12),
        color="black",
    )
    ax.hlines(
        ranged_df["Low"],
        ranged_df["Date"] - timedelta(hours=12),
        ranged_df["Date"] + timedelta(hours=12),
        color="black",
    )
    ax.bar(
        ranged_df["Date"],
        height=abs(ranged_df["Open"] - ranged_df["Close"]),
        bottom=ranged_df[["Open", "Close"]].min(axis=1),
        color=(ranged_df["Open"] > ranged_df["Close"]).map(
            {True: "red", False: "green"}
        ),
        width=1,
    )

    # Volume
    ax2 = ax.twinx()
    ax2.set_ylabel(f"Volume (in: {volume_scale}s)")
    ax2.set_xlim(x_lim_start, x_lim_end)
    ax2.set_ylim(y_lim_start, y_lim_end)

    ax2.bar(
        ranged_df["Date"],
        ranged_df["Volume"],
        label="Volume",
        color="blue",
        alpha=0.1
    )

    mplcursors.cursor(hover=True).connect(
        "add",
        lambda sel: sel.annotation.set_text(
            f"Date: {df.index[sel.index]}\n"
            f"O: {ranged_df['Open'][sel.index]}\n"
            f"H: {ranged_df['High'][sel.index]}\n"
            f"L: {ranged_df['Lose'][sel.index]}\n"
            f"C: {ranged_df['Close'][sel.index]}"
        ),
    )

    plt.show()


df = get_stock_data("stocks", "AAPL")
display_stock_df(df)
