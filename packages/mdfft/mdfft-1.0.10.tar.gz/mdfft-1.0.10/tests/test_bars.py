import unittest
from datetime import datetime, timedelta, timezone
from .base_test import BaseTestCase

class TestCandles(BaseTestCase):

    DT_FMT = '%Y-%m-%d %H:%M:%S'

    def test_candle_ts(self):
        c = self._candles().head()
        self.assertEqual(c.timestamp, 915192000)

    def test_get_price_as_str(self):
        c = self._candles().head()
        self.assertEqual(c['o'], 113.25)
        self.assertEqual(c['h'], 113.25)
        self.assertEqual(c['l'], 113.2)
        self.assertEqual(c['c'], 113.24)


    def test_common(self):
        candles = self._candles()
        self.assertEqual(candles.candles_count(), 11)

        b = candles.head()
        self.assertEqual(b.dt_as_str(self.DT_FMT), '1999-01-01 12:00:00')

        b = candles.tail()
        self.assertEqual(b.dt_as_str(self.DT_FMT), '2008-01-04 08:00:00')

    def test_prices(self):
        candles = self._candles()

        b = candles.head().next().next()
        self.assertEqual(b.open,  113.2400)
        self.assertEqual(b.high, 113.4800)
        self.assertEqual(b.low, 113.2400)
        self.assertEqual(b.close, 113.4800)

        b.price_coeff = 100
        self.assertEqual(b.open, 11324)

    def test_navigation(self):

        candles = self._candles()

        b = candles.head()
        self.assertEqual(b.dt_as_str(self.DT_FMT), '1999-01-01 12:00:00')
        b = b.next()
        self.assertEqual(b.dt_as_str(self.DT_FMT), '1999-01-01 13:00:00')
        b = b.next()
        self.assertEqual(b.dt_as_str(self.DT_FMT), '1999-01-01 15:00:00')

        b = candles.tail()
        self.assertEqual(b.dt_as_str(self.DT_FMT), '2008-01-04 08:00:00')
        b = b.prev()
        self.assertEqual(b.dt_as_str(self.DT_FMT), '1999-01-04 07:00:00')
        b = b.prev()
        self.assertEqual(b.dt_as_str(self.DT_FMT), '1999-01-04 06:00:00')

        self.assertIsNone(candles.tail().next())
        self.assertIsNone(candles.head().prev())

    def test_find(self):

        candles = self._candles()
        b = candles.head().next().next(3)

        fdt = datetime.strptime(b.dt_as_str(self.DT_FMT), self.DT_FMT)
        fdt = fdt.replace(tzinfo=timezone.utc)
        fb = candles.find_candle(fdt)
        self.assertTrue(b.eq(fb))
        self.assertFalse(b.prev().eq(fb))

        fb = candles.find_candle(datetime.now(tz=timezone.utc))
        self.assertIsNone(fb)

    def test_find_bar_from_bar(self):
        candles = self._candles()
        b = candles.head().next().next()
        fdt = datetime.strptime(b.dt_as_str(self.DT_FMT), '%Y-%m-%d %H:%M:%S')
        fdt = fdt.replace(tzinfo=timezone.utc)

        fb = candles.find_candle(fdt)
        self.assertIsNotNone(fb)

        fb = candles.find_candle(fdt, b)
        self.assertIsNotNone(fb)

        fb = candles.find_candle(fdt, b.next())
        self.assertIsNone(fb)

    def test_find_nearly(self):
        candles = self._candles()
        b = candles.head().next().next()

        bdt = datetime.strptime(b.dt_as_str(self.DT_FMT), '%Y-%m-%d %H:%M:%S')
        bdt = bdt.replace(tzinfo=timezone.utc)
        pdt = bdt - timedelta(minutes=1)

        pb = candles.find_candle(pdt, nearly=True)
        self.assertIsNotNone(pb)
        self.assertEqual(pb, b.prev())

        ndt = pdt + timedelta(minutes=1)
        nb = candles.find_candle(ndt, nearly=True)
        self.assertIsNotNone(nb)
        self.assertEqual(nb, b)

    def test_range(self):
        candles = self._candles()

        r = candles.range_dt()
        self.assertIsNone(r)

        sb = candles.head().next()
        eb = candles.tail()
        r = candles.range_dt(sb.datetime, eb.datetime)
        self.assertTrue(r.head().eq(sb))
        self.assertTrue(r.tail().eq(eb))

        r = candles.range_dt(sb.datetime)
        self.assertTrue(r.tail().eq(candles.tail()))
        self.assertTrue(r.head().eq(sb))

        r = candles.range_dt(dt_end=eb.datetime)
        self.assertTrue(r.tail().eq(eb))
        self.assertTrue(r.head().eq(candles.head()))

    def test_height_low(self):
        candles = self._candles()

        hb, lb = candles.high_and_low_candles()
        self.assertIsNotNone(hb)
        self.assertIsNotNone(lb)

        self.assertEqual(hb.high, 114)
        self.assertEqual(lb.low, 112.7500)

        candles = candles.range_candles(candles.head(), candles.head().next())
        hb, lb = candles.high_and_low_candles()
        self.assertEqual(hb.high, 113.25)
        self.assertEqual(lb.low, 113.2)

    def test_find_left_bar(self):

        candles = self._candles()
        b = candles.find_candle_before(
            datetime(year=1999, month=1, day=1, hour=14, tzinfo=timezone.utc)
        )
        self.assertIsNotNone(b)
        self.assertEqual(b.hour, 13)

        b = candles.find_candle_before(
            datetime(year=1999, month=1, day=1, hour=12, tzinfo=timezone.utc)
        )
        self.assertIsNotNone(b)
        self.assertEqual(b.hour, 12)

        b = candles.find_candle_before(
            datetime(year=1999, month=1, day=1, hour=11, tzinfo=timezone.utc)
        )
        self.assertIsNone(b)

        b = candles.find_candle_before(
            datetime(year=2099, month=1, day=1, hour=11, tzinfo=timezone.utc)
        )
        self.assertIsNotNone(b)
        self.assertEqual(b.hour, 8)
        self.assertEqual(b.year, 2008)

        from_b = candles.head().next().next()
        b = candles.find_candle_before(
            datetime(year=1999, month=1, day=1, hour=19, tzinfo=timezone.utc),
            from_b
        )
        self.assertEqual(str(from_b), str(b))

        from_b = candles.head().next().next()
        b = candles.find_candle_before(
            datetime(year=1999, month=1, day=4, hour=19, tzinfo=timezone.utc),
            from_b
        )
        self.assertEqual(b.hour, 7)

    def test_change_tf(self):
        candles = self._candles()

        candles2h = candles.to_tf('3h')
        self.assertIsNotNone(candles2h)
        self.assertEqual(candles2h.head().hour, 12)
        self.assertEqual(candles2h.head().next().hour, 15)
        self.assertEqual(candles2h.head().next(3).day, 4)
        self.assertEqual(candles2h.tail().year, 2008)

        candles1d = candles.to_tf('1d')
        self.assertIsNotNone(candles1d)
        self.assertEqual(candles1d.head().day, 1)
        self.assertEqual(candles1d.head().next().day, 4)
        self.assertEqual(candles1d.head().next(2).year, 2008)

    def test_concat(self):
        candles = self._candles()
        candles2 = candles.range_candles(candle_start=candles.tail())
        self.assertEqual(candles2.candles_count(), 1)
        candles3 = candles.concat(candles2)
        self.assertEqual(candles3.candles_count(), candles.candles_count() + 1)
        b1 = candles3.tail()
        b2 = candles3.tail().prev()
        self.assertEqual(str(b1), str(b2))


if __name__ == '__main__':
    unittest.main()
