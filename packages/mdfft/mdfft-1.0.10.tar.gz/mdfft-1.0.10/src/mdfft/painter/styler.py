from dataclasses import dataclass, field

@dataclass
class Styler:
    """Class keep information abount candle style colors, line style and etc..."""

    color_background: str = field(init=False, default='white')

    color_bear_body: str = 'black'
    color_bear_border: str = 'black'
    style_bear_body_border: str = '-'
    color_bear_shadow: str = 'black'
    style_bear_shadow: str = '-'

    color_bull_body: str = 'white'
    color_bull_border: str = 'black'
    style_bull_body_border: str = '-'
    style_bull_shadow: str = '-'
    color_bull_shadow: str = 'black'

    bar_width: float = field(init=False, default=0.6)
    bar_shadow_width: float = field(init=False, default=1)

    dt_format: str = field(init=False, default="%d-%m-%Y\n%H:%M")

    marker_size: int = field(init=False, default=8)
    marker_color: str = field(init=False, default='green')
    marker: str = field(init=False, default='8')

    line_style: str = field(init=False, default='solid')
    line_color: str = field(init=False, default='green')
