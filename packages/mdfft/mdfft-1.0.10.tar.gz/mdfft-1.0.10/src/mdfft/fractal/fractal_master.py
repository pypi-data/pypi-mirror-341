from dataclasses import dataclass
from .fractal import Fractal
from .fractal_line import FractalLine

@dataclass
class FractalMaster:
    candles_cnt : int = 2

    def fractal(self, candle):
        """
        Is this fractal candle or not
        @param candle: Candle
        @return frac: Fractal
        """

        if (candle.index <= self.candles_cnt) or (candle.index_back <= self.candles_cnt):
            return None

        # Upper candles
        up_frac = True
        last_price_left = candle.high
        last_price_right = candle.high
        for ci in range(1, self.candles_cnt + 1):
            bhl = candle.prev(ci).high
            if bhl >= last_price_left:
                up_frac = False
                break

            bhr = candle.next(ci).high
            if bhr >= last_price_right:
                up_frac = False
                break

        # Down candles
        down_candle = True
        last_price_left = candle.low
        last_price_right = candle.low
        for ci in range(1, self.candles_cnt + 1):
            bll = candle.prev(ci).low
            if bll <= last_price_left:
                down_candle = False
                break

            blr = candle.next(ci).low
            if blr <= last_price_right:
                down_candle = False
                break

        # Result
        if up_frac and down_candle:
            return Fractal(Fractal.FRAC_BOTH, candle)
        if up_frac:
            return Fractal(Fractal.FRAC_UP, candle)
        if down_candle:
            return Fractal(Fractal.FRAC_DOWN, candle)
        return None

    def line(self, start_candle, frac_cnt=1, inverse=False):
        """Fractal line"""

        step_size = -1 if inverse else 1
        fracs = []
        c = start_candle.clone()
        ccnt = 1
        while (c is not None) and (len(fracs) < frac_cnt):
            frac = self.fractal(c)
            c = c.step(step_size)
            if frac is None:
                ccnt = ccnt + 1
                continue

            if frac.type in [Fractal.FRAC_UP, Fractal.FRAC_BOTH]:
                frac.type = Fractal.FRAC_UP
                frac.prev_candles_cnt = ccnt - 1
                fracs.append(frac)

            if frac.type in [Fractal.FRAC_DOWN, Fractal.FRAC_BOTH]:
                frac.type = Fractal.FRAC_DOWN
                frac.prev_candles_cnt = ccnt - 1
                fracs.append(frac)

            ccnt = 1

        if len(fracs) != frac_cnt:
            return None

        if inverse:
            fracs.reverse()

        return FractalLine(fracs)

    def last_line(self, start_candle, fracs_cnt=1):
        return self.line(start_candle, frac_cnt=fracs_cnt, inverse=True)

    def find_line(self, line, candle, max_lines=10, exact=True):
        frac_cnt = line.count(Fractal.FRAC_UP) + line.count(Fractal.FRAC_DOWN)
        lines = []
        c = candle.clone()
        while (c is not None) and (len(lines) < max_lines):
            found_line = self.line(c, frac_cnt)
            if found_line is None:
                break
            if found_line.eq_line(line, exact):
                lines.append(found_line)

            c = found_line.second_frac_candle

        return lines
