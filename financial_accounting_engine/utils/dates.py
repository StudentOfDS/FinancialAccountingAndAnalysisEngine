import pandas as pd


def to_datetime(value):
    return pd.to_datetime(value, errors="raise")
