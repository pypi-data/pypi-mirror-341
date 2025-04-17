import unittest
from mdfft import SimpleParser, Candles, TimeFrame, painter as p

class BaseTestCase(unittest.TestCase):

    def _candles(self):
        parser = SimpleParser(file='./tests/bars.txt')
        return Candles.from_raw_candles(
                parser.parse(),
                timeframe=TimeFrame('1H')
        )

    def _candles_fractals(self):
        parser = SimpleParser(file='./tests/bars_fractal.txt')
        return Candles.from_raw_candles(
                parser.parse(),
                timeframe=TimeFrame('1H')
        )

    def _draw_candles(self):
        p.start_paint()
        p.paint(self._candles())
        p.paint_done()

    def _draw_candles_fractal(self):
        p.start_paint()
        p.paint(self._candles_fractals())
        p.paint_done()
