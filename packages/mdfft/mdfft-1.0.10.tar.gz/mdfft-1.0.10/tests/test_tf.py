import unittest
from datetime import datetime
from mdfft import TimeFrame
from .base_test import BaseTestCase


class TestTf(BaseTestCase):

    def test_create_tf(self):
        TimeFrame("1H")
        TimeFrame("12H")
        TimeFrame("1D")
        TimeFrame("1W")
        TimeFrame("1MONTH")

        self.assertRaises(Exception, TimeFrame, "66M")
        self.assertRaises(Exception, TimeFrame, "0M")
        self.assertRaises(Exception, TimeFrame, "35M")
        self.assertRaises(Exception, TimeFrame, "0H")
        self.assertRaises(Exception, TimeFrame, "13H")
        self.assertRaises(Exception, TimeFrame, "0D")
        self.assertRaises(Exception, TimeFrame, "2D")
        self.assertRaises(Exception, TimeFrame, "0W")
        self.assertRaises(Exception, TimeFrame, "2W")
        self.assertRaises(Exception, TimeFrame, "0MONTH")
        self.assertRaises(Exception, TimeFrame, "2MONTH")

    def test_parse(self):
        (u, t) = TimeFrame.parse_tf('1W')
        self.assertEqual(u, 1)
        self.assertEqual(t, 'W')

        (u, t) = TimeFrame.parse_tf('w')
        self.assertEqual(u, 1)

        (u, t) = TimeFrame.parse_tf('2h')
        self.assertEqual(u, 2)
        self.assertEqual(t, 'H')

        (u, t) = TimeFrame.parse_tf('m5')
        self.assertEqual(u, 5)
        self.assertEqual(t, 'M')

    def test_allow_change(self):

        tf = TimeFrame('1H')
        self.assertTrue(tf.allow_change_order('1D'))
        self.assertTrue(tf.allow_change_order('2H'))
        self.assertTrue(tf.allow_change_order('1MONTH'))

        tf = TimeFrame('1MONTH')
        self.assertFalse(tf.allow_change_order('1D'))
        self.assertFalse(tf.allow_change_order('2H'))
        self.assertFalse(tf.allow_change_order('1W'))

    def test_close_period(self):

        n = datetime.now()
        tf = TimeFrame('1H')
        c_dt = tf.close_period(n)
        self.assertEqual(c_dt.hour, n.hour)
        self.assertEqual(c_dt.minute, 59)
        self.assertEqual(c_dt.day, n.day)

        n = datetime.now().replace(hour=14)
        tf = TimeFrame('2H')
        c_dt = tf.close_period(n)

        self.assertEqual(c_dt.hour, n.hour+1)
        self.assertEqual(c_dt.day, n.day)
        self.assertEqual(c_dt.minute, 59)

        n = datetime(year=2022, month=5, day=13)
        tf = tf = TimeFrame('1W')
        c_dt = tf.close_period(n)
        self.assertEqual(c_dt.hour, 23)
        self.assertEqual(c_dt.minute, 59)
        self.assertEqual(c_dt.day, 15)

        n = datetime(year=2022, month=5, day=13)
        tf = TimeFrame('1MONTH')
        c_dt = tf.close_period(n)
        self.assertEqual(c_dt.hour, 23)
        self.assertEqual(c_dt.minute, 59)
        self.assertEqual(c_dt.day, 31)
        self.assertEqual(c_dt.month, 5)

        # n = datetime(year=2022, month=12, day=13)
        # tf = TimeFrame('3MONTH')
        # c_dt = tf.close_period(n)
        # self.assertEqual(c_dt.hour, 23)
        # self.assertEqual(c_dt.minute, 59)
        # self.assertEqual(c_dt.day, 28)
        # self.assertEqual(c_dt.month, 2)
        # self.assertEqual(c_dt.year, 2023)

    def test_next_open_period(self):
        tf = TimeFrame('1D')
        n = datetime(year=2022, month=12, day=13)
        n = tf.next_period(n)
        self.assertEqual(n.day, 14)
        n = tf.next_period(n)
        self.assertEqual(n.day, 15)

    def test_change_to_month_tf(self):
        tf = TimeFrame("1MONTH")
        n = datetime(year=1999, month=11, day=1)
        c_dt = tf.close_period(n)
        self.assertEqual(c_dt.year, 1999)
        self.assertEqual(c_dt.month, 11)
        self.assertEqual(c_dt.day, 30)
        self.assertEqual(c_dt.hour, 23)
        self.assertEqual(c_dt.minute, 59)

        # tf = TimeFrame("3MONTH")
        # c_dt = tf.close_period(n)
        # self.assertEqual(c_dt.year, 2000)
        # self.assertEqual(c_dt.month, 1)
        # self.assertEqual(c_dt.day, 31)
        # self.assertEqual(c_dt.hour, 23)
        # self.assertEqual(c_dt.minute, 59)

if __name__ == '__main__':
    unittest.main()
