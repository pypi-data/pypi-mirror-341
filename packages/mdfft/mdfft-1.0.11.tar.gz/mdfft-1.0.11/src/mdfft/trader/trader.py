
class Trader:
    """
    Platform for trading simu;ate
    """
    PLACE_TYPE_BUY = 'B'
    PLACE_TYPE_SELL = 'S'

    def place_order(self, candle, order_price, place_type, sl, tp, tl=None):
        """
        Place a order after candle
        @param order_price: Open price
        @param place_type: str - Order type buy or sell. See PLACE_TYPE_* constants
        @param sl: float - Stop loss
        @param tp: float - Take profit
        @param tl: int - Order time to live
        @return: Pips, candles count, action price
        """
        if isinstance(order_price, str):
            order_price = candle[order_price]
        open_price = order_price
        action_price = open_price
        b = candle.clone()
        dist = 0
        tl = 256 << 20 if tl is None or tl <= 0 else tl

        while b is not None:

            if dist > tl:
                break

            if ((b.low <= sl and place_type == self.PLACE_TYPE_BUY) or
                (b.high >= sl and place_type == self.PLACE_TYPE_SELL)):
                action_price = sl
                break

            if ((b.high >= tp and place_type == self.PLACE_TYPE_BUY) or
                (b.low <= tp and place_type == self.PLACE_TYPE_SELL)):
                action_price = tp
                break

            dist = dist + 1
            action_price = b.close
            b = b.next()

        if place_type == self.PLACE_TYPE_BUY:
            return action_price - open_price, dist, action_price
        if place_type == self.PLACE_TYPE_SELL:
            return open_price - action_price, dist, action_price
        return None
