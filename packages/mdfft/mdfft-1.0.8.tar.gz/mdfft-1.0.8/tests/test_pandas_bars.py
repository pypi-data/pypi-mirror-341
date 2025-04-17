import sys
sys.path.insert(0, './src/')
import pandas as pd
from mdfft import SimpleParser, Candles, PandasCandles
from .base_test import BaseTestCase


class TestBars(BaseTestCase):

    def load_df(self):
        q = pd.read_csv(
            'tests/bars.txt',
            sep=' ',
            header=None,
            names=['date', 'time', 'o', 'h', 'l', 'c'],
            dtype={'date': 'str', 'time': 'str'})
        q.date = q.date.apply(
            lambda r: '19' + r if r[0] == '9' else '20' + r[1:])
        q.time = q.time.apply(lambda r: '0' + r if len(r) == 3 else r)
        q = q.assign(
            dt=pd.to_datetime(q.date + ' ' + q.time, format='%Y%m%d %H%M'))
        q.drop(['date', 'time'], axis=1, inplace=True)
        return q

    def test_pandas_df_to_bars(self):
        df = self.load_df()
        self.assertEqual(df.shape[0], 11)
        candles = PandasCandles.pandas_df_to_candles(df, '1h')
        self.assertIsNotNone(candles)
        self.assertEqual(candles.candles_count(), 11)
        self.assertEqual(candles.head().open, df.iloc[0]['o'])
        self.assertEqual(candles.head().close, df.iloc[0]['c'])
        self.assertEqual(candles.head().datetime, df.iloc[0]['dt'])
        self.assertEqual(candles.tail().open, df.iloc[10]['o'])
        self.assertEqual(candles.tail().close, df.iloc[10]['c'])
        self.assertEqual(candles.tail().datetime, df.iloc[10]['dt'])

    def test_window_pandas(self):
        bars = Candles.from_raw_candles(
                SimpleParser(file='tests/bars.txt').parse(), timeframe='1H')
        df = PandasCandles.candles_windows_to_pandas_df(bars, 3)
        self.assertIsNotNone(df)
        self.assertEqual(df.loc[0]['open2'], 113.25)
        self.assertEqual(df.loc[0]['open1'], 113.21)
        self.assertEqual(df.loc[0]['open'], 113.24)
        self.assertEqual(df.loc[1]['open'], 113.32)
        self.assertEqual(df.loc[2]['open'], 112.82)
