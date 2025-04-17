import re
from .fractal import Fractal

class FractalLine():
    __fracs = []

    def __init__(self, fracs):
        sorted_frac = sorted(fracs, key=lambda f: f.price)
        for f in fracs:
            f.line_index = sorted_frac.index(f) + 1
        self.__fracs = fracs

    def title(self):
        return "".join([f"{f.type:s}{f.line_index:d}" for f in self.__fracs])

    def line_width(self):
        return "".join(["{f.type:s}{f.line_index:d}:{f.prev_candles_cnt:d}"
            for f in self.__fracs])

    @property
    def fracs(self):
        return self.__fracs

    @property
    def first_frac_candle(self):
        return self.fracs[0].candle

    @property
    def last_frac_candle(self):
        return self.fracs[-1].candle

    @property
    def second_frac_candle(self):
        return self.fracs[1].candle

    @classmethod
    def inverse_title(cls, line):
        match = re.findall(r'([{Fractal.FRAC_UP}|{Fractal.FRAC_DOWN}]\d+)', line)
        match_cnt = len(match)
        line = []
        for m in match:
            line.append(Fractal.FRAC_DOWN if m[0] == Fractal.FRAC_UP else Fractal.FRAC_UP)
            line.append(str(match_cnt - int(m[1:]) + 1))
        return "".join(line)

    @classmethod
    def inverse_line_width(cls, line):
        match = re.findall(r'([{Fractal.FRAC_UP}|{Fractal.FRAC_DOWN}]\d+:\d+)', line)
        match_cnt = len(match)
        line = []
        for m in match:
            line.append(Fractal.FRAC_DOWN if m[0] == Fractal.FRAC_UP else Fractal.FRAC_UP)
            (p, w) = m[1:].split(":")
            line.append(str(match_cnt - int(p) + 1) + ":" + str(w))
        return "".join(line)

    def eq_line(self, title, exact=False):
        my_title = self.title()
        return (title == my_title) or (not exact and (title == FractalLine.inverse_title(my_title)))

    def eq_line_with_width(self, line, exact=False):
        my_line = self.line_width()
        invers_my_line = FractalLine.inverse_line_width(my_line)
        return (line == my_line) or ((not exact) and (line == invers_my_line ))
