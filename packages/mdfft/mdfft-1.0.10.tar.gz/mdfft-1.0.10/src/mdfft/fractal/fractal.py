class Fractal:
    """The class represents a technical analysis fractal.
    More information about fractals can be found in the literature on technical analysis by Bill Williams
    """

    FRAC_UP = 'U'
    FRAC_DOWN = 'D'
    FRAC_BOTH = 'B'
    FRAC_NONE = 'N'

    __candle = None
    __type = FRAC_NONE
    __line_index = 1     # Index in array
    __prev_candles_cnt = 0  # Count of prev candles

    def __init__(self, frac_type, candle, line_index=1):
        self.__candle = candle
        self.__type = frac_type
        self.__line_index = line_index
        self.__prev_candles_cnt = 0

    def __str__(self):
        return f"{self.__type}{str(self.__candle)}"

    @property
    def prev_candles_cnt(self):
        return self.__prev_candles_cnt

    @prev_candles_cnt.setter
    def prev_candles_cnt(self, value):
        """
        May be wrong if fractal line made with inverse mode
        """
        self.__prev_candles_cnt = value

    @property
    def line_index(self):
        return self.__line_index

    @line_index.setter
    def line_index(self, value):
        value = int(value)
        if value <= 0:
            raise ValueError("Value mast greeter than 0")
        self.__line_index = value

    @property
    def candle(self):
        return self.__candle

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        if value not in [Fractal.FRAC_UP, Fractal.FRAC_DOWN]:
            raise ValueError("Bad type")
        self.__type = value

    @property
    def price(self):
        if self.__type in [Fractal.FRAC_UP, Fractal.FRAC_BOTH]:
            return self.__candle.high
        if self.__type == Fractal.FRAC_DOWN:
            return self.__candle.low
        raise ValueError("Cant determine price")
