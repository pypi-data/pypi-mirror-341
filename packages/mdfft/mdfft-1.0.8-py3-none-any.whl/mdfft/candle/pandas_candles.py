import pandas as pd
from ..parsers import RawCandle
from .candles import Candles

class PandasCandles:
    """The class that converts candles collection to Pandas dataframe and back."""

    @classmethod
    def candles_to_pandas_df(cls, candles):
        return pd.DataFrame(
            {
                'open':  [b.o for b in candles],
                'close': [b.c for b in candles],
                'high':  [b.h for b in candles],
                'low':   [b.l for b in candles],
                'dt':   [b.dt for b in candles]
            },
            index=[b.index for b in candles]
        )

    @classmethod
    def candles_windows_to_pandas_df(cls, candles, window_len, start_candle=None,
                                     exclude_columns=None):
        if exclude_columns is not None:
            exclude_columns = exclude_columns.lower()
        else:
            exclude_columns = ''

        windows = candles.windows(window_len, start_candle=start_candle)

        df_struct = {}
        for i in range(window_len):
            n = window_len - i - 1
            if n == 0:
                n = ''

            if 'o' not in exclude_columns:
                df_struct[f"open{n}"] = [wc[i].o for wc in windows]
            if 'h' not in exclude_columns:
                df_struct[f"high{n}"] = [wc[i].h for wc in windows]
            if 'l' not in exclude_columns:
                df_struct[f"low{n}"] = [wc[i].l for wc in windows]
            if 'c' not in exclude_columns:
                df_struct[f"close{n}"] = [wc[i].c for wc in windows]
            if 'dt' not in exclude_columns:
                df_struct[f"dt{n}"] = [wc[i].dt for wc in windows]

        return pd.DataFrame(df_struct, index=list(range(len(windows))))

    @classmethod
    def pandas_df_to_candles(cls, df, tf, o='o', h='h', l='l', c='c', dt='dt'):
        df = df.reset_index()
        return Candles.from_raw_candles(
            [RawCandle(row[dt], row[o], row[h], row[l], row[c]) for index, row in df.iterrows()],
            timeframe=tf
        )