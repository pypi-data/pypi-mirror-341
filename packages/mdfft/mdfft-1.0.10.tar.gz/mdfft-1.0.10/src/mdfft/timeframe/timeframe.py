import re
from datetime import timedelta, datetime


class TimeFrame:

    M_SUFFIX = 'M'  # Minue
    H_SUFFIX = 'H'  # Hour
    D_SUFFIX = 'D'  # Day
    W_SUFFIX = 'W'  # Week
    MONTH_SUFFIX = 'MONTH'  # Month

    TF_ORDER = [M_SUFFIX, H_SUFFIX, D_SUFFIX, W_SUFFIX, MONTH_SUFFIX]

    TF_UNITS = {
        M_SUFFIX: [1,2,3,4,5,6,10,15,20,30],
        H_SUFFIX: [1,2,3,4,6,8,12],
        D_SUFFIX: [1],
        W_SUFFIX: [1],
        MONTH_SUFFIX: [1]
    }

    __RE_UNIT = r'(\d?\d?)'
    __RE_SUFFIX = r'(M|H|D|W|MONTH)'

    __delta = timedelta(microseconds=1)
    __tf = '1M'

    @classmethod
    def parse_tf(cls, tf):

        plan = [
            [
                r'^\s*' + cls.__RE_UNIT + cls.__RE_SUFFIX + r'\s*$',
                1, 2
            ],
            [
                r'^\s*' + cls.__RE_SUFFIX + cls.__RE_UNIT + r'\s*$',
                2, 1
            ],
        ]

        for p in plan:
            mr = re.match(p[0], tf, re.IGNORECASE)
            if mr is not None:
                unit = mr.group(p[1])
                if unit == '':
                    unit = 1
                unit = int(unit)
                suffix = mr.group(p[2]).upper()

                return unit, suffix
        return None, None

    @classmethod
    def tf(cls, tf):
        if isinstance(tf, str):
            return TimeFrame(tf)
        return tf

    def __init__(self, tf):
        u, s = TimeFrame.parse_tf(tf)
        if u and s:
            if u in TimeFrame.TF_UNITS.get(s,[]):
                self.__tf = tf
                return
        raise ValueError("Bad timeframe tf")

    def __str__(self):
        return f"{self.unit()}{self.suffix()}"

    def __eq__(self, other):
        if not isinstance(other, TimeFrame):
            return NotImplemented

        return self.unit() == other.unit() and self.suffix() == other.suffix()

    def unit(self):
        u, _ = self.parse_tf(self.__tf)
        return u

    def suffix(self):
        _, s = self.parse_tf(self.__tf)
        return s

    def allow_change_order(self, new_tf):
        new_tf = TimeFrame.tf(new_tf)
        u_new = new_tf.unit()
        s_new = new_tf.suffix()

        order_new = self.TF_ORDER.index(s_new)
        order_curr = self.TF_ORDER.index(self.suffix())

        if order_new < order_curr:
            return False
        if order_new == order_curr:
            return u_new > self.unit()
        return True

    def close_period(self, dt):
        u = self.unit()
        s = self.suffix()
        c_dt = self.open_period(dt)
        if s == self.M_SUFFIX:
            c_dt = c_dt + timedelta(minutes=u)
        elif s == self.H_SUFFIX:
            c_dt = c_dt + timedelta(hours=u)
        elif s == self.D_SUFFIX:
            c_dt = c_dt + timedelta(days=u)
        elif s == self.W_SUFFIX:
            c_dt = c_dt - timedelta(days=c_dt.weekday())
            c_dt = c_dt + timedelta(days=7 * u)
        elif s == self.MONTH_SUFFIX:
            month = c_dt.month + u - 1
            year = c_dt.year + month // 12
            month = month % 12 + 1
            c_dt = datetime(year=year, month=month, day=1)
        else:
            raise ValueError('Wrong timestamp suffix')
        return c_dt - self.__delta

    def open_period(self, dt):
        s = self.suffix()
        c_dt = dt
        if s == self.M_SUFFIX:
            b = dt.minute // self.unit()
            c_dt = c_dt.replace(minute=b*self.unit(), second=0, microsecond=0)
        elif s == self.H_SUFFIX:
            b = dt.hour // self.unit()
            c_dt = c_dt.replace(hour=b*self.unit(), minute=0, second=0, microsecond=0)
        elif s == self.D_SUFFIX:
            c_dt = c_dt.replace(hour=0, minute=0, second=0, microsecond=0)
        elif s == self.W_SUFFIX:
            c_dt = c_dt.replace(hour=0, minute=0, second=0, microsecond=0)
            c_dt = c_dt - timedelta(days=c_dt.weekday())
        elif s == self.MONTH_SUFFIX:
            c_dt = c_dt.replace(hour=0, minute=0, second=0, microsecond=0, day=1)
        else:
            raise ValueError('Wrong timestamp suffix')
        return c_dt

    def next_period(self, dt):
        return self.close_period(dt) + self.__delta
