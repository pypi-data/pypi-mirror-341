from ..parsers import RawCandle
from ..timeframe import TimeFrame
from .candle import Candle

class Candles:
    """
    The class represents a candles collection
    """
    __PREVIEW_CANDLES_CNT = 6

    __raw_candles = []
    __candles_count = 0
    __candle_index = None
    __price_coeff = 1

    def __init__(self, raw_candles=None, timeframe='1M', price_coeff=1,
                 array=None):
        if raw_candles is None:
            raw_candles = []

        if array:
            for i in range(array.shape[0] // 5):
                raw_candles.append(RawCandle(
                    array[i * 4],
                    array[i * 4 + 1],
                    array[i * 4 + 2],
                    array[i * 4 + 3],
                    array[i * 4 + 4]))

        self.__raw_candles = raw_candles
        self.__candles_count = len(raw_candles)
        self.__price_coeff = price_coeff
        self.__timeframe = TimeFrame.tf(timeframe)

    def __repr__(self):
        table = "dt o h l c\n"
        cc = self.candles_count()
        pcc = Candles.__PREVIEW_CANDLES_CNT
        if cc > pcc:
            top_indices = range(0, pcc//2)
            middle_line = "...\n"
            bottom_indices = range(cc-1, cc-(pcc//2)-1, -1)
        else:
            bottom_indices = []
            top_indices = range(0, cc)
            middle_line = ""

        for ci in top_indices:
            table = table + repr(self._mk_candle(ci)) + "\n"
        table = table + middle_line
        for ci in reversed(bottom_indices):
            table = table + repr(self._mk_candle(ci)) + "\n"

        table = table + "___\n" + f"Total: {self.candles_count()}\n"

        return table

    def __getitem__(self, key):
        if isinstance(key, int):
            if 0 > key >= self.candles_count():
                raise IndexError("Wrong candle index")
            return self.candle_at(key)

        if isinstance(key, slice):
            start, stop, _ = key.indices(self.candles_count())
            return self.range_candles(self.candle_at(start), self.candle_at(stop-1))

        raise ValueError("Wrong key type")

    def __iter__(self):
        self.__candle_index = 0
        return self

    def __next__(self):
        if self.__candle_index >= self.__candles_count:
            raise StopIteration

        self.__candle_index += 1
        return self._mk_candle(self.__candle_index - 1)

    def __len__(self):
        return self.__candles_count

    @classmethod
    def from_raw_candles(cls, candles, timeframe='1M', price_coeff=1):
        return Candles(raw_candles=candles, price_coeff=price_coeff,
                       timeframe=timeframe)

    @classmethod
    def from_array(cls, array, timeframe='1M', price_coeff=1 ):
        return Candles(array=array, price_coeff=price_coeff,
                       timeframe=timeframe)

    @property
    def price_coeff(self):
        return self.__price_coeff

    @price_coeff.setter
    def price_coeff(self, coeff):
        self.__price_coeff = coeff

    @property
    def timeframe(self):
        return self.__timeframe

    @property
    def raw_candles(self):
        return self.__raw_candles


    def _mk_candle(self, inx):
        """Wrapper over create candle function. Uses for passing original candle costructor parameters."""
        return Candle(self.__raw_candles, inx, self.__price_coeff)

    def append_candle(self, raw_candle=None, dt=None, o=None, h=None, l=None,
                      c=None):
        if dt is not None:
            self.__raw_candles.append(RawCandle(dt, o, h, l, c))
        if raw_candle is not None:
            self.__raw_candles.append(raw_candle)
        self.__candles_count = len(self.__raw_candles)


    def head(self):
        """Get a first candle object"""
        return self._mk_candle(0)

    def tail(self):
        """Get a last candle object"""
        return self._mk_candle(self.__candles_count-1)

    def candles_count(self):
        """Get a candles count"""
        return self.__candles_count

    def candle_at(self, index):
        if index >= self.__candles_count:
            raise IndexError(f'No bar at index {index}')
        return self._mk_candle(index)

    def candle_exists(self, candle_dt):
        return self.find_candle(candle_dt) is not None

    def find_candle(self, candle_dt, from_candle=None, nearly=False):
        """Search candle by date"""
        if candle_dt is None:
            return None

        lft = 0 if from_candle is None else from_candle.index
        rht = self.__candles_count
        while rht - lft > 1:
            m = (lft + rht) // 2
            if candle_dt < self._mk_candle(m).datetime:
                rht = m
            else:
                lft = m
        candle = self._mk_candle(lft)
        if nearly or candle.datetime == candle_dt:
            return candle
        return None

    def find_candle_before(self, dt, start_candle=None):
        """Search a candle that is early or equal date."""

        if start_candle is None:
            start_candle = self.head()
        tail_candle = self.tail()

        # If the passed date is less than the first candle date, then None
        if dt < start_candle.datetime:
            return None

        # If the passed date is greater than or equal to the date of the last bar,
        # then will return the most recent candle.
        if dt >= tail_candle.datetime:
            return self.tail()

        # Find the first bar whose date is less than the passed one
        b = start_candle
        while b is not None:
            if b.datetime > dt:
                return b.prev()
            b = b.next()
        return b

    def range_candles(self, candle_start=None, candle_end=None):
        """Create a candle collection that between passed dates"""
        if candle_start is None and candle_end is None:
            return None
        if candle_start is None:
            candle_start = self.head()
        if candle_end is None:
            candle_end = self.tail()

        return Candles.from_raw_candles(
            self.raw_candles[candle_start.index:candle_end.index + 1],
            self.timeframe,
            self.price_coeff)

    def range_dt(self, dt_start=None, dt_end=None, ):
        """Range candles between dates"""
        return self.range_candles(self.find_candle(dt_start), self.find_candle(dt_end))

    def skip(self, cnt):
        """Returns the candles collection, skipping the specified first ones."""
        return self.range_candles(self.head().next(cnt), self.tail())

    def take(self, limit, skip=0, from_candle=None):
        """Returns a collection of candles by skipping the first specified ones."""
        if from_candle is None:
            from_candle = self.head()
        if limit == 0:
            return None
        if skip > 0:
            from_candle = from_candle.next(skip)

        raw_candles = []
        c = from_candle
        for _ in range(limit):
            if c is None:
                break
            raw_candles.append(c.raw_candle)
            c = c.next()
        return Candles.from_raw_candles(raw_candles, self.timeframe, self.price_coeff)

    def __set_candle_index(self, index):
        self.__candle_index = index

    def high_and_low_candles(self):
        """Returns a high and a low candles"""
        candle_inx = self.__candle_index
        self.__set_candle_index(0)
        high_candle = self.head()
        low_candle = self.tail()
        for b in self:
            if b.high > high_candle.high:
                high_candle = b

            if b.low < low_candle.low:
                low_candle = b
        self.__set_candle_index(candle_inx)
        return high_candle, low_candle

    def to_tf(self, new_tf):
        """Change a timeframe and return a new candles collection with a new timeframe"""
        new_tf = TimeFrame.tf(new_tf)
        if not self.__timeframe.allow_change_order(new_tf):
            raise ValueError('Cant change timeframe. Old: '+
                             str(self.timeframe)+
                             " New:"+
                             str(new_tf))

        raw_candles = []
        start_candle = self.head()
        while start_candle is not None:
            close_date = new_tf.close_period(start_candle.datetime)
            end_candle = self.find_candle_before(close_date, start_candle)
            range_candles = self.range_candles(start_candle, end_candle)
            high_candle, low_candle = range_candles.high_and_low_candles()
            raw_candles.append(
                RawCandle(
                    new_tf.open_period(start_candle.datetime),
                    o=start_candle.open,
                    h=high_candle.high,
                    l=low_candle.low,
                    c=end_candle.close
                )
            )
            start_candle = end_candle.next()

        return Candles.from_raw_candles(raw_candles, new_tf, self.__price_coeff)

    def windows(self, window_len, start_candle=None):
        """Returning a window candles array"""

        if start_candle is None:
            start_candle = self.head()

        windows = []
        while start_candle is not None:
            end_candle = start_candle.next(window_len)
            if end_candle is None:
                break

            candles = self.range_candles(start_candle, end_candle)
            if candles is None:
                break
            windows.append(candles)

            start_candle = start_candle.next()

        return windows

    def concat(self, another_candles):
        """Concat two candle collections"""
        if another_candles.timeframe != self.timeframe:
            raise ValueError('Not equalent time frames')
        if another_candles.price_coeff != self.price_coeff:
            raise ValueError('Not eualent price coefs')
        return Candles.from_raw_candles(
            self.raw_candles + another_candles.raw_candles,
            self.timeframe,
            self.price_coeff,
        )