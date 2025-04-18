import datetime

class Candle:
    """
    The class represents a single market candle with different attributes.
    """

    # Types of direct of candle
    DIRECT_BEAR = 'bears'
    DIRECT_BULL = 'bull'
    DIRECT_DOJI = 'doji' # Open price == Close price

    __DT_FORMAT = '%Y.%m.%d %H:%M'

    __ATTRS_MAP = {
        'o':  'open',
        'c':  'close',
        'h':  'high',
        'l':  'low',
        'm':  'mid',
        'dt': 'datetime',
        'i':  'index',
        'ib': 'index_back',
        'd':  'direct'
    }
    __candle = {}
    __candles = None
    __index = None
    __price_coeff = 1
    __tz=datetime.timezone.utc

    def __init__(self, candles_list, index, price_coeff=1, tz=datetime.timezone.utc):
        if not candles_list:
            raise ValueError('Empty candles list')

        self.__candles = candles_list
        self.__index = index
        self.__candle = candles_list[index]
        self.__price_coeff = price_coeff
        self.__tz = tz

    def __repr__(self):
        return "".join((
            f"{self.dt_as_str()}",
            " ",
            f"{self.open} {self.high} {self.low} {self.close}"
        ))

    def __str__(self):
        return repr(self)

    def __getitem__(self, key):
        if isinstance(key, str):
            return self.__getattr__(key)
        raise AttributeError(f"Wrong key {key}")

    def __getattr__(self, key):
        attr = Candle.__ATTRS_MAP.get(key, key)
        if attr not in self.__ATTRS_MAP.values():
            raise AttributeError(f"Cant find attr {key}")
        return getattr(self, attr)

    def __hash__(self):
        return repr(self)

    def __eq__(self, other):
        if isinstance(other, Candle):
            return repr(self) == repr(other)
        raise NotImplementedError(f"Your cant compare with {other.__class__.__name__}")

    @property
    def index(self):
        return self.__index

    @property
    def index_back(self):
        return len(self.__candles) - self.__index

    @property
    def raw_candle(self):
        return self.__candles[self.__index]

    @property
    def candles(self):
        return self.__candles

    @property
    def open(self):
        return self.__candle.o * self.__price_coeff

    @property
    def high(self):
        return self.__candle.h * self.__price_coeff

    @property
    def low(self):
        return self.__candle.l * self.__price_coeff

    @property
    def close(self):
        return self.__candle.c * self.__price_coeff

    @property
    def year(self):
        return self.datetime.year

    @property
    def month(self):
        return self.datetime.month

    @property
    def day(self):
        return self.datetime.day

    @property
    def minute(self):
        return self.datetime.minute

    @property
    def hour(self):
        return self.datetime.hour

    @property
    def datetime(self):
        dt = self.__candle.dt.replace(second=0, microsecond=0)
        return dt.astimezone(self.__tz)

    @property
    def timezone(self):
        return self.__tz

    @property
    def timestamp(self):
        return int(self.__candle.dt.timestamp())

    @property
    def date(self):
        return self.datetime.date()

    @property
    def time(self):
        return self.datetime.time()

    @property
    def mid(self):
        if self.direct == Candle.DIRECT_DOJI:
            return self.open

        mid_abs = abs(self.open - self.close) / 2
        if self.direct == Candle.DIRECT_BEAR:
            return mid_abs + self.close

        return mid_abs + self.open

    def dt_as_str(self, fmt=None):
        return self.datetime.strftime(Candle.__DT_FORMAT if fmt is None else fmt)

    @property
    def direct(self):
        if self.open > self.close:
            return self.DIRECT_BEAR
        if self.open < self.close:
            return self.DIRECT_BULL
        if self.open == self.close:
            return self.DIRECT_DOJI
        return None

    def step(self, step_size):
        new_index = self.__index + step_size
        if (new_index >= len(self.__candles)) or (new_index < 0):
            return None
        return Candle(self.__candles, new_index, self.__price_coeff, self.__tz)

    def next(self, num=1):
        return self.step(abs(num))

    def prev(self, num=1):
        return self.step(0 - abs(num))

    @property
    def price_coeff(self):
        return self.__price_coeff

    @price_coeff.setter
    def price_coeff(self, coeff=1):
        self.__price_coeff = coeff

    def clone(self):
        return Candle(self.__candles, self.__index, self.__price_coeff, self.__tz)

    def eq(self, other_candle):
        return repr(self) == repr(other_candle)
