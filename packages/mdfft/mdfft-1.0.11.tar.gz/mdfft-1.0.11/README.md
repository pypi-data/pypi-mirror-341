# Market Data Form Finder Toolkit (MDFFT)

The project goal is to make working with a raw market data easier. Provide a tool that allow to identify recurrent market patterns.
Any types of market can processed by this.

The library allow to carry out following tasks:
* Load a list of quotes for any instrument.
* Create a chart using the Japanese candlestick format.
* Draw lines and markers on the chart.
* Search for candles using various criteria.
* Navigate through the entire candles collection.
* Change the timeframe to different one.

## Table of content
 - [Install](#install)
 - [Import classes](#import_classes)
 - [Candle collection examples](#cc)
   - [Load candles collection](#cc_load)
   - [Candles count](#cc_count)
   - [First and last candles](#cc_first_and_last)
   - [Get candle by index](#cc_get_candle_by_index)
   - [Navigation through dataset](#cc_navigation)
   - [Search candle by date](#cc_search_by_date)
   - [Subcollection by index](#cc_sub_collection_by_index)
   - [Subcollection by date](#cc_sub_collection_by_date)
   - [Iteration over collection](#cc_iteration)
   - [High and low candles in collection](#cc_high_and_low)
- [Timeframes](#tf)
  - [Timeframe of candles collection](#tf_current)
  - [Change timeframe](#tf_change)
- [Pandas](#pd)
  - [Create pandas dataset from collection](#pd)
- [Candle](#c)
  - [Prev and next candle](#c_next_and_prev)
  - [Candle type](#c_type)
  - [Candle prices](#c_prices)
  - [Candle time](#c_dt)
  - [Candle index](#c_index)
- [Candle chart](#ct)
  - [Simple chart](#ct_simple)
  - [Save chart to file](#ct_save)
  - [Chart appearance](#ct_tune)
  - [Draw on chart](#ct_draw_on_chart)
- [Trading](#t)

<a id="install"></a>
## Install ##

```bash
 pip install mdfft
```

<a id="import_classes"></a>
## Import classes

The namespace **mdfft** contains of whole list of lib's classes. The example of import is below:

```python
from mdfft import Candles, SimpleParser, Styler, painter as p, RawCandle, Trader
```

Classes:
* Candle - The class represents a Japanese candle
* Candles - The class represents a Japanese candle list
* RawCandle - The simple class that based to create Candle. May used in quote parsers.
* painter - The object to draw a chart.
* Style - The class to appearance a chart.
* SimpleParser - The class to parse candles for my samples.

<a id="cc"></a>
## Candle collection examples ##

<a id="cc_load"></a>
### Load candles ###

The collection of candles is created by parsing quotes or making an array of RawCandle objects. The array of RawCandles is created by the programmer himself.
> [!NOTE]
> datetime object must be in the UTC time zone. If you are not set a timezone then error occurred.
> Please pay attention to the use of time zones to avoid errors.

```python
   raw_candles = [
        RawCandle(
            dt=datetime(2020, 1, 1,
                tzinfo=timezone.utc), # Candle datetime with timezone
            o=2,                      # Open price
            h=4,                      # High price
            l=1,                      # Low price
            c=3                       # Close price
        ),
        RawCandle(
            dt=datetime(2020, 1, 2,
                tzinfo=timezone.utc), # dt
            o=12,                     # ohlc prices
            h=14,
            l=11,
            c=13
        )
    ]

    # Now candles in America/Lima timezone
    # If tz is not set than use local zone
    candles = Candles.from_raw_candles(raw_candles, timeframe="1D", tz='America/Lima')
    print(candles)
```

Next I will use my SimpleParser and my rather large data set of OHLC quotes.
By default candles is in local time zone

```python
 parser = SimpleParser(file="./data/EURUSD_H1.txt")
 candles = Candles.from_raw_candles(parser.parse(), timeframe="1H")
```

<a id="cc_count"></a>
#### Count of candles in the dataset

```python
    print(candles.candles_count())
    print(len(candles))
```

<a id="cc_first_and_last"></a>
#### A first and a last candle in the dataset

```python
    start_candle = candles.head()
    print("Start candle: " + str(start_candle))

    end_candle = candles.tail()
    print("End candle: " + str(end_candle))
```

<a id="cc_get_candle_by_index"></a>
#### Get a candle by an index

```python
    my_candle = candles.candle_at(1985)
    same_candle = candles[1985]
```

<a id="cc_navigation"></a>
#### Navigation through a dataset

Navigation is performed by calling ``next()`` and ```prev()``` methods of a candle object.

```python
    next_candle = my_candle.next()
    prev_candle = my_candle.prev()
    next20_candle = my_candle.next(20)
    prev30_candle = my_candle.prev(30)
```

<a id="cc_search_by_date"></a>
#### Search by a date

Exact search.
```python
    found_candle = candles.find_candle(datetime(1999, 1, 4, 5))
    if not found_candle:
        print("Candle not found at 1999-01-04 05:00")
    return print("Found candle: " + str(found_candle))
```

Finds a candle whose date is greater than the given
```python
    found_candle = candles.find_candle(datetime(1999, 1, 4, 6), nearly=True)
    return print("Found candle: " + str(found_candle))
```


<a id="cc_sub_collection_by_index"></a>
#### Get a subcollection from the main collection by indices

```python
    # take 10 skip 5 candles
    print(candles.take(10, skip=5))
    # or  print(candles[5:15])

    # skip 5 candles from collection
    print(candles.skip(5))
    # or  print(candles[5:])
```

<a id="cc_sub_collection_by_date"></a>
#### Get a subcollection from the main collection by dates

```python
    from datetime import datetime
    # New candles collection from 2000-01-01 to 2000-01-10
    # Note Only if candles are exists

    candles_range = candles.range_dt( datetime(2000, 1, 3,  1 ), datetime(2000, 1, 10, 1))
    if not candles_range:
        print("No candles in range")
        return 0
    print("Count candles: " + str(candles_range.candles_count()))
    print(candles_range)
```

<a id="cc_iteration"></a>
#### Iterate over a collection ####

```python
    # Iterate candles
    for candle in candles:
        print("Candle: " + str(candle))
```

<a id="cc_high_and_low"></a>
#### A highest and a lowest candle in the collection

```python
    # Get the high candle and the low candle
    candle_h, candle_l = candles.high_and_low_candles()
    print("High candle: " + str(candle_h))
    print("Low candle: " + str(candle_l))
```

<a id="tf"></a>
### Timeframes

A candle collection may be converted from a current timeframe to another timeframe. A new timeframe must be bigger than the source timeframe.

Example: the timeframe of 1 hour **may be** converted to 2 hours, 8 hours, 1 day, or another one, but bigger than source one.
The 1 hour timeframe **must not** convert to 45 minutes, 30 minutes, or another one less.

A timeframe label consists of two parts: a number of time units and a time unit label.

Example of timeframes: _20M_ - 29 minutes timeframe, _1H_ - 1 hour timeframe, _3H_ - 11 hours timeframe, _1D_ - 1 day timeframe

Possible time unit labels:
* **M** - minute
* **H** - hour
* **D** - day
* **W** - week
* **MONTH** - month

Possible timeframes units:
* For minute - 1,2,3,4,5,6,10,15,20,30
* For hours - 1,2,3,4,6,8,12
* Other - only 1

<a id="tf_current"></a>
#### Get a timeframe of a candles collection

```python
    print(candles.timeframe)
```

<a id="tf_change"></a>
#### Change a candles collection timeframe

```python
    candles_3h  = candles_1h.to_tf("3H")
    candles_4h  = candles_3h.to_tf("4H")
    candles_12h = candles_4h.to_tf("12H")
    candles_1d  = candles_4h.to_tf("1D")
```

<a id="pd"></a>
### Pandas

Convert a candles collection to a pandas dataframe

```python
    from mdfft import PandasCandles

    df = PandasCandles.candles_to_pandas_df(candles)
    print(df)
```

You may create a dataset in which a row contains several candles prices.

```python
    from mdfft import PandasCandles

    # 3 candles in a single row
    df_windows = PandasCandles.candles_windows_to_pandas_df(candles, 3)
    print(df_windows)
```

<a id="c"></a>
### Candle ###

<a id="c_next_and_prev"></a>
#### Next and prev candle

```python
    # Candle at 1985 index
    candle = candles.candle_at(1985)

    # Next candle
    next_candle = candle.next()

    # 30 candles to forward
    next30_candle = candle.next(30)

    # Prev candle
    prve_candle = candle.prev()

    # Prev 100 candle
    prev100_candle = candle.prev(100)
```

<a id="c_type"></a>
#### Candle type

```python
    # bull/bear/doji see constants in Candle.DIRECT_*
    direct = candle.direct # or candle.d or candle['d']  print(direct)
```

<a id="c_prices"></a>
#### Prices ####

```python
    # All prices different methods
    price_open = candle.open   # or candle.o or candle['o']
    price_high = candle.high   # or candle.h or candle['h']
    price_low = candle.low     # or candle.l or candle['l']
    price_close = candle.close # or candle.c or candle['c']
    price_mid = candle.mid     # or candle.m or candle['m']
```

<a id="c_dt"></a>
#### Dates and times

```python
    # Returns datetime object
    candle_dt = candle.datetime # or candle.dt or candle['dt']
    candle_date = candle.date
    candle_time = candle.time

    # Returns int
    candle_year   = candle.year
    candle_month  = candle.month
    candle_day    = candle.day
    candle_hour   = candle.hour
    candle_minute = candle.minute

    # Date time format
    dt_str = candle.dt_as_str()
    print(dt_str)

    dt_str_fmt = candle.dt_as_str('%d, %b %Y')
    print(dt_str_fmt)

    # Timestamp
    ts = candle.timestamp()
    print(ts)

    ts_utc = candle.timestamp_utc()
    print(ts_utc)
```

<a id="c_index"></a>
#### Candle index

```python
    # Candle index from start
    ci = candle.index # or candle.i or candle['i']

    # Candle index from back
    cib = candle.index_back # or candle.ib or candle['ib']
```

<a id="ct"></a>
### Candle chart

To start painting you **must** import bellow classes

```python
    from mdfft import painter as p, Styler
```

Matplotlib is used for drawing. That means you may use colors, marker, visual elements, etc. from Matplotlib.


<a id="ct_simple"></a>
#### Simple chart

```python
    p.start_paint()
    p.title="Candles"
    p.paint(candles_collection)
    p.paint_done()
```

<a id="ct_save"></a>
#### Save chart to file

```python
    p.start_paint()
    p.title = "Save paint"
    p.paint(candles_to_paint)
    p.save_paint('candles.jpg')
```

<a id="ct_tune"></a>
#### Appearance

The appearance is performed through the object of class Styler that included in object painter. Possible settings is an enum in class Styler.

```python
    # The appearance of the chart is configured through the object Styler
    # Each candle has own the color of body, shadow and border
    s = Styler()
    p.title="Rainbow candles"
    s.color_bear_body =   [plt.cm.get_cmap('Pastel1', candles_cnt)(c) for c in range(candles_cnt)]
    s.color_bear_border = [plt.cm.get_cmap('Set1_r',  candles_cnt)(c) for c in range(candles_cnt)]
    s.color_bear_shadow = "blue"
    s.color_bull_body =   [plt.cm.get_cmap('turbo',   candles_cnt)(c) for c in range(candles_cnt)]
    s.color_bull_border = [plt.cm.get_cmap('tab20b',  candles_cnt)(c) for c in range(candles_cnt)]
    s.color_bull_shadow = "green"

    # Apply style
    p.styler = s

    # Draw candles
    p.start_paint()
    p.paint(candles)
    p.paint_done()
```

<a id="ct_draw_on_chart"></a>
#### Drawing on the chart

Possible markers and lines

```python
    p.start_paint()

    # Paint candles
    p.paint(candles_to_paint)

    # Paint markers for each 5 candles
    for c in candles_to_paint:
        if (c.index % 5) == 0:
            p.paint_marker(c, "l", marker_size=4, marker_color='red', marker='v')
            p.paint_marker(c, "h", marker_size=3, marker_color='black', marker='^')
            p.paint_marker(c, c.mid, marker='_')

    # Paint line. From hightest price to lowest price
    hc, lc = candles_to_paint.high_and_low_candles()
    p.paint_line( hc, hc.high, lc, lc.low, line_style="dotted", line_color="green")

    # Show picture
    p.paint_done()
```

<a id="t"></a>
### Trading

For the success or failure of a position, the Trader class is used. The class contains a single method that returns the result of a position at a certain point.

```python
    pip = 1 / 10000
    start_candle = candles.candle_at(12345)
    trader = Trader()

    profit, distance, action_price = trader.place_order(
        candle=start_candle,              # candle for order, not datetime
        order_price='o',                  # open price - possible 'o' 'h' 'l' 'c' OR float
        place_type=Trader.PLACE_TYPE_BUY, # PLACE_TYPE_BUY or PLACE_TYPE_SELL
        sl=start_candle.low - pip,        # stop loss
        tp=start_candle.high + pip * 100, # take profit
        tl=1000                           # candles before force close. time to live position
    )

    # My profit. Positive or negative
    print(f"Profit pips: {profit / pip}")

    # Candles from start before close order
    print(f"Candles to close order: {distance}")

    # Price that close order
    print(f"Price that close order: {action_price}")
```
