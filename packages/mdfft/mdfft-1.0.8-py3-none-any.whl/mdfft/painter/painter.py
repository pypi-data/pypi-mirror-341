from dataclasses import dataclass, field
import matplotlib.pyplot as plt
from ..candle.pandas_candles import PandasCandles
from .styler import Styler
import warnings

@dataclass
class Painter:

    styler: Styler = field(init=False, default_factory=lambda: Styler())
    title: str = field(init=False, default='')
    __fig = None
    __candles = None

    def start_paint(self, height=600, width=800, dpi=100):
        h_inch = height // dpi
        w_inc = width // dpi
        self.__fig = plt.figure(figsize=(w_inc, h_inch), dpi=dpi)

    def __close_paint(self):
        self.__candles = None
        plt.close()

    def paint_done(self):
        self.__fig.tight_layout()
        plt.show()
        self.__close_paint()

    def save_paint(self, fn):
        self.__fig.tight_layout()
        plt.savefig(fn)
        self.__close_paint()

    def __check_candles_before_painting(self):
        if self.__candles is None:
            raise AttributeError("Draw candles before drawing the marker")

    def paint_line(self, start_bar, start_price, end_bar, end_price,
                   line_color=None, line_style=None):
        if isinstance(start_price, str):
            start_price = start_bar[start_price]
        if isinstance(end_price, str):
            end_price = end_bar[end_price]

        self.__check_candles_before_painting()
        start_candle = self.__candles.find_candle(start_bar.dt)
        if start_candle is None:
            warnings.warn("Start candle not found in painting candles")
            return

        end_candle = self.__candles.find_candle(end_bar.dt)
        if end_candle is None:
            warnings.warn("End candle not foun in painting candles")
            return

        plt.plot(
            (start_candle.index, end_candle.index),
            (start_price, end_price),
            color=self.styler.line_color if line_color is None else line_color,
            ls=self.styler.line_style if line_style is None else line_style
        )

    def paint_marker(self, candle, price=None, marker=None, marker_size=None,
                     marker_color=None):
        if price is None:
            price = candle.mid
        elif isinstance(price, str):
            price = candle[price]

        self.__check_candles_before_painting()

        c = self.__candles.find_candle(candle.dt)
        if c is None:
            warnings.warn("A marker candle not found in drawing candles")
            return

        if marker is None:
            marker = self.styler.marker
        if marker_size is None:
            marker_size = self.styler.marker_size
        if marker_color is None:
            marker_color = self.styler.marker_color

        plt.plot(c.index, price,
                 antialiased=False,
                 marker=marker,
                 markersize=marker_size,
                 markerfacecolor=marker_color,
                 markeredgecolor=marker_color)

    def paint(self, candles, take=100, skip=0):
        skip = max(skip, 0)
        styler = self.styler
        working_candles = candles.take(take, skip=skip)
        self.__candles = working_candles
        df = PandasCandles.candles_to_pandas_df(working_candles)
        up = df[df.close >= df.open]
        down = df[df.close < df.open]
        plt.bar(
            up.index,
            up.close - up.open,
            styler.bar_width,
            bottom=up.open,
            color=styler.color_bull_body,
            edgecolor=styler.color_bull_border,
            ls=styler.style_bull_body_border)
        plt.plot(
            [up.index, up.index],
            [up.close, up.high],
            color=styler.color_bull_shadow,
            linewidth=styler.bar_shadow_width,
            ls=styler.style_bull_shadow)
        plt.plot(
            [up.index, up.index],
            [up.open, up.low],
            color=styler.color_bull_shadow,
            linewidth=styler.bar_shadow_width,
            ls=styler.style_bull_shadow)
        plt.bar(
            down.index,
            down.open - down.close,
            styler.bar_width,
            bottom=down.close,
            color=styler.color_bear_body,
            edgecolor=styler.color_bear_border,
            ls=styler.style_bear_body_border)
        plt.plot(
            [down.index, down.index],
            [down.open, down.high],
            color=styler.color_bear_shadow,
            linewidth=styler.bar_shadow_width,
            ls=styler.style_bear_shadow)
        plt.plot(
            [down.index, down.index],
            [down.close, down.low],
            color=styler.color_bear_shadow,
            linewidth=styler.bar_shadow_width,
            ls=styler.style_bear_shadow)

        plt.xticks(rotation=45, ha='center')

        ax = plt.gca()
        ax.set_aspect('auto')
        ax.set_xticklabels([b.datetime.strftime(self.styler.dt_format) for b in working_candles])
        if self.title:
            plt.title(self.title)
        return ax
