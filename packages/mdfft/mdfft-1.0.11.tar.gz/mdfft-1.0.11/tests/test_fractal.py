import unittest
from mdfft import FractalMaster, FractalLine, Fractal, painter as p
from .base_test import BaseTestCase


class TestFractal(BaseTestCase):

    def test_fractals(self):
        f = FractalMaster()
        self.assertEqual(f.fractal(self._candles_fractals().candle_at(6)).type, Fractal.FRAC_UP)
        self.assertEqual(f.fractal(self._candles_fractals().candle_at(3)).type, Fractal.FRAC_DOWN)
        self.assertIsNone(f.fractal(self._candles_fractals().candle_at(0)))
        self.assertIsNone(f.fractal(self._candles_fractals().candle_at(1)))
        self.assertIsNone(f.fractal(self._candles_fractals().candle_at(2)))
        self.assertIsNone(f.fractal(self._candles_fractals().candle_at(7)))
        self.assertIsNone(f.fractal(self._candles_fractals().candle_at(10)))

    def test_fractal_line(self):
        f = FractalMaster()
        l = f.line(self._candles_fractals().head(), 4)
        self.assertEqual(l.title(), "D2U4D3D1")
        #  p.start_paint()
        #  p.title = l.title()
        #  p.paint(self._candles_fractals())
        #  for f in l.fracs:
        #      p.paint_marker(f.candle, f.price, marker_size=f.prev_candles_cnt)
        #  p.paint_done()

    def test_fractal_empty_line(self):
        f = FractalMaster()
        l = f.line(self._candles_fractals().candle_at(21), 2)
        self.assertIsNone(l)

    def test_inverse(self):
        self.assertEqual(FractalLine.inverse_title("U1D2"), "D2U1")
        self.assertEqual(FractalLine.inverse_title("U3D2U1"), "D1U2D3")

    def test_inverse_width(self):
        self.assertEqual(FractalLine.inverse_line_width("U1:4D2:23"), "D2:4U1:23")
        self.assertEqual(FractalLine.inverse_line_width("U3:11D2:4U1:1"), "D1:11U2:4D3:1")

    def test_eq(self):
        f = FractalMaster()
        l = f.line(self._candles_fractals().head(), 2)
        self.assertTrue(l.eq_line("D1U2"))
        self.assertFalse(l.eq_line("D2U1"))

    def test_find_line(self):
        f = FractalMaster()

        lines = f.find_line("D1U2", self._candles_fractals().head(), exact=True)
        self.assertEqual(len(lines), 2)

        lines = f.find_line("D1U2", self._candles_fractals().head(), exact=False)
        self.assertEqual(len(lines), 3)

        #  p.start_paint()
        #  p.paint(self._candles_fractals())
        #  li = 0
        #  colors = ['red', 'green', 'yellow']
        #  for l in lines:
        #      for f in l.fracs:
        #          p.paint_marker(f.candle, f.price + 0.04 * li, marker_color=colors[li])
        #      li = li + 1
        #  p.paint_done()

    def test_find_line_second(self):
        f = FractalMaster()

        lines = f.find_line("D1U3D2", self._candles_fractals().head(), exact=True)
        self.assertEqual(len(lines), 1)

    def test_find_last_lane(self):
        f = FractalMaster()

        last_line = f.last_line(self._candles_fractals().head().next(), 3)
        self.assertIsNone(last_line)

        last_line = f.last_line(self._candles_fractals().tail(), 3)
        self.assertIsNotNone(last_line)
        self.assertEqual(last_line.title(), "D2D1U3")


if __name__ == '__main__':
    unittest.main()
