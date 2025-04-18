# Run from main dir
import sys
sys.path.insert(0, '../src/')

import locale
import matplotlib as plt
from datetime import datetime, timezone
from mdfft import Candles, SimpleParser, Styler, painter as p, RawCandle, Trader, PandasCandles

# Range_dt if candles not exists

def trader():
    
    parser = SimpleParser(file="./data/EURUSD_H1.txt")
    candles = Candles.from_raw_candles(parser.parse(), timeframe="1H")

    pip = 1 / 10000
    start_candle = candles.candle_at(12345)
    
    trader = Trader()
    profit, distance, action_price =  trader.place_order(
        candle=start_candle,
        order_price='o', # o h l c OR float
        place_type=Trader.PLACE_TYPE_BUY,
        sl=start_candle.low - pip,
        tp=start_candle.high + pip * 100,
        tl=1000 # after 1000 candles order closed
    )

    print(f"Profit pips: {profit / pip}")
    print(f"Candles to close order: {distance}")
    print(f"Price that close order: {action_price}")

def painter():

    parser = SimpleParser(file="./data/EURUSD_H1.txt")
    candles = Candles.from_raw_candles(parser.parse(), timeframe="1H")

    candles_cnt = 100
    candles_to_paint = candles.take(candles_cnt, skip=1000)

    p.start_paint()
    p.title="Candles"
    p.paint(candles_to_paint)
    p.paint_done()
    #
    # #
    p.start_paint()
    p.title = "Save paint"
    p.paint(candles_to_paint)
    p.save_paint('/tmp/candles.jpg')
   
    s = Styler()
    p.title="Rainbow candles"
    s.color_bear_body =   [plt.cm.get_cmap('Pastel1', candles_cnt)(c) for c in range(candles_cnt)]
    s.color_bear_border = [plt.cm.get_cmap('Set1_r',  candles_cnt)(c) for c in range(candles_cnt)]
    s.color_bear_shadow = "blue"
    s.color_bull_body =   [plt.cm.get_cmap('Blues',    candles_cnt)(c) for c in range(candles_cnt)]
    s.color_bull_border = [plt.cm.get_cmap('Accent',  candles_cnt)(c) for c in range(candles_cnt)]
    s.color_bull_shadow = "green"
    p.styler = s

    # https://matplotlib.org/stable/api/markers_api.html#
    p.start_paint()
    p.paint(candles_to_paint)
    for c in candles_to_paint:
        if (c.index % 20) == 0:
            p.paint_marker(c, "l", marker_size=4, marker_color='red', marker='v')
            p.paint_marker(c, "h", marker_size=4, marker_color='black', marker='^')
            p.paint_marker(c, c.mid, marker='_')
    p.paint_done()

    #
    p.start_paint()
    p.paint(candles_to_paint)
    p.title = "Lines"
    p.paint_line(candles_to_paint.head(), 'o', candles_to_paint.tail(), 'l')

    hc, lc = candles_to_paint.high_and_low_candles()
    p.paint_line( hc, hc.high, lc, lc.low, line_style="dotted", line_color="green")
    p.paint_done()
    #
    # Savefig


def parser():

    raw_candles = [
        RawCandle(
            dt=datetime(2020, 1, 1, tzinfo=timezone.utc),
            o=2,
            h=4,
            l=1,
            c=3
        ),
        RawCandle(
            dt=datetime(2020, 1, 2, tzinfo=timezone.utc),
            o=12,
            h=14,
            l=11,
            c=13
        )
    ]
    candles = Candles.from_raw_candles(raw_candles, timeframe="1D")

    parser = SimpleParser(file="./data/EURUSD_H1.txt")
    candles = Candles.from_raw_candles(parser.parse(), timeframe="1H")

def candle():
    # Load Candles
    parser = SimpleParser(file="./data/GBPUSD_H1.txt")
    candles = Candles.from_raw_candles(parser.parse(), timeframe="1H")

    # Get candle
    candle = candles.candle_at(1985)
    #
    # Next candle
    next_candle = candle.next()

    # 30 candles to forward
    next30_candle = candle.next(30)

    # Prev candle
    prve_candle = candle.prev()

    # Prev 100 candle
    prev100_candle = candle.prev(100)
    #
    #  # Candle direct bull/bear/doji
    direct = candle.direct # bull/bear/doji
    print(direct)

    #  # Prices
    price_open = candle.open # or  candle.o or candle['o']
    price_high = candle.high # or candle.h or candle['h']
    price_low = candle.low # or candle.l or candle['l']
    price_close = candle.close # or candle.c or candle['c']
    price_mid = candle.mid # candle.m or candle['m']
    print(price_open, price_high, price_low, price_close, price_mid)
    #
    #  # Index in candles collections
    #  print(f"index in candles {candle.index()}")
    #  print(f"index from back {candle.index_back()}")
    
    #  # Datetimes
    candle_dt = candle.datetime # or candle.dt or candle['dt']
    candle_date = candle.date 
    candle_time = candle.time
    print(candle_dt, candle_date, candle_time)

    candle_year = candle.year
    candle_month = candle.month
    candle_day = candle.day
    candle_hour = candle.hour
    candle_minute = candle.minute

    dt_str = candle.dt_as_str()
    print(dt_str)

    dt_str_fmt = candle.dt_as_str("%d, %b %Y")
    print(dt_str_fmt)

    # Index

    #  # Index and index from back
    ci = candle.index # or candle.i or candle['i']

    cib = candle.index_back # or candle.ib or candle['ib']
    print(ci, cib)

def candles():

    # Load Candles
    parser = SimpleParser(file="./data/USDJPY_H1.txt")
    candles = Candles.from_raw_candles(parser.parse(), timeframe="1H")

    # Candles count
    print(candles.candles_count())
    print(len(candles))

    # Start and stop
    start_candle = candles.head()
    print("Start candle: " + str(start_candle))
    end_candle = candles.tail()
    print("End candle: " + str(end_candle))

    # Candle at index
    my_candle = candles.candle_at(1985)
    same_candle = candles[1985]
    print(my_candle == same_candle and my_candle.eq(same_candle))

    # Next and prev
    next_candle = my_candle.next()
    prev_candle = my_candle.prev()

    next20_candle = my_candle.next(20)
    prev30_candle = my_candle.prev(30)
    
    # Found candles
    found_candle = candles.find_candle(
        datetime(1999, 1, 4, 5, tzinfo=timezone.utc)
    )
    if not found_candle:
        print("Candle not found at 1999-01-04 05:00")
        return 
    print("Found candle: " + str(found_candle))

    # Sub set
    print("take 10 skip 5 candles")
    print(candles.take(10, skip=5))
    # or
    print(candles[5:15])

    # skip 5 candles from collection
    print("skip 5 candles from range")
    print(candles.skip(5))
    # or
    print(candles[5:])

def timeframe():

    # Load Candles
    parser = SimpleParser(file="./data/USDJPY_H1.txt")
    candles = Candles.from_raw_candles(parser.parse(), timeframe="1H")

    # Current timeframe
    print(candles.timeframe)

    print(candles.head().datetime )
    print(candles.head().dt_as_str() )
    # Change timeframe
    candles_2h = candles.to_tf("2H")
    candles_3h = candles_2h.to_tf("3H")
    candles_4h = candles_3h.to_tf("4H")
    candles_12h = candles_4h.to_tf("12H")
    print(candles_12h)

def pandas():

    # Load Candles
    parser = SimpleParser(file="./data/USDJPY_H1.txt")
    candles = Candles.from_raw_candles(parser.parse(), timeframe="1H")

    # pandas df
    df = PandasCandles.candles_to_pandas_df(candles)
    print(df)

    # windows to pandas df
    df_windows = PandasCandles.candles_windows_to_pandas_df(candles, 3)
    print(df_windows)


def main() -> int:

    trader()
    painter()
    parser()
    candles()
    candle()
    timeframe()
    pandas()
    return 0

if __name__ == "__main__":
    sys.exit(main())
