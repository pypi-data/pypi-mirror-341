import unittest
from mdfft import painter as p, Trader
from .base_test import BaseTestCase

class TestOrder(BaseTestCase):

    def test_place_order_buy_tp(self):

        start_candle = self._candles_fractals().candle_at(3)
        close_price = 114
        trader = Trader()
        pips, dist, _ = trader.place_order(
            start_candle,
            'o',
            Trader.PLACE_TYPE_BUY,
            start_candle.low - 0.0001,
            close_price
        )
        close_bar = start_candle.next(dist)

        #  p.start_paint()
        #  p.paint(self._candles_fractals())
        #  p.paint_marker(start_candle, start_candle.open)
        #  p.paint_marker(close_bar, close_price)
        #  p.paint_line(start_candle, 'o', close_bar, 'h', line_color='red', line_style='dotted')
        #  p.paint_done()
        #
        self.assertEqual(close_price - start_candle.open, pips)

    def test_place_order_buy_sl(self):
        start_candle = self._candles_fractals().candle_at(1)
        end_candle = self._candles_fractals().candle_at(6)
        #  p.start_paint()
        #  p.paint(self._candles_fractals())
        #  p.paint_marker(start_candle, start_candle.open)
        #  p.paint_marker(end_candle, end_candle.close)
        #  p.paint_done()

        trader = Trader()
        pips, _, _ = trader.place_order(
            start_candle,
            'o',
            Trader.PLACE_TYPE_BUY,
            start_candle.low,
            end_candle.high
        )

        self.assertEqual(start_candle.low - start_candle.open, pips)

    def test_place_order_buy_ttl(self):
        start_candle = self._candles_fractals().candle_at(1)
        end_candle = self._candles_fractals().candle_at(7)

        pips, dist, close_price = Trader().place_order(
            start_candle,
            'o',
            Trader.PLACE_TYPE_BUY,
            0,
            115,
            6
        )

        #  p.start_paint()
        #  p.paint(self._candles_fractals())
        #  p.paint_marker(start_candle, start_candle.open)
        #  p.paint_marker(end_candle, end_candle.close)
        #  p.paint_marker(start_candle.next(dist), close_price, marker_color="red")
        #  p.paint_done()

        self.assertEqual(end_candle.close - start_candle.open, pips)

    def test_place_order_buy_none(self):
        start_candle = self._candles_fractals().candle_at(0)
        end_candle = self._candles_fractals().tail()

        trader = Trader()
        pips, _, _ = trader.place_order(
            start_candle,
            'o',
            Trader.PLACE_TYPE_BUY,
            111,
            116
        )
        self.assertEqual(end_candle.close - start_candle.open, pips)

    def test_place_order_dist(self):

        bars = self._candles_fractals().take(17, 2)
        start_candle = bars.candle_at(1)
        end_candle = bars.candle_at(15)

        _, dist, close_price = Trader().place_order(
            start_candle,
            'c',
            Trader.PLACE_TYPE_BUY,
            0,
            end_candle.high - 0.0001
        )

        #  p.start_paint()
        #  p.paint(bars)
        #  p.paint_marker(start_candle, 'c')
        #  p.paint_marker(end_candle, close_price)
        #  p.paint_line(start_candle, 'c', start_candle.next(dist), close_price, line_color='red')
        #  p.paint_done()
        #
        self.assertEqual(dist, end_candle.index - start_candle.index)


if __name__ == '__main__':
    unittest.main()
