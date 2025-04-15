class BuyOrder:
    def __init__(self, entry_price, quantity, stoploss=None, takeprofit=None, traling_stop_loss: bool = False, 
            trailing_take_profit: bool = False, entry_date=None):
        self.entry_price = entry_price
        self.entry_date = entry_date
        self.quantity = quantity
        self.stoppercent = stoploss
        self.stoploss = (1-stoploss)*entry_price if stoploss is not None else None
        self.takeprofit = (1+takeprofit)*entry_price if takeprofit is not None else None
        self.status = 'open'
        self.type = 'buy'
        self.trailing_stop_loss = traling_stop_loss
        self.trailing_take_profit = trailing_take_profit
    def close(self, close_price, close_date=None):
        self.close_date = close_date
        self.close_price = close_price
        self.pl = self.quantity * (self.close_price - self.entry_price)
        self.status = 'closed'
    def check(self, current_price):
        if self.trailing_stop_loss:
            if (current_price - self.stoploss) > (self.entry_price - self.stoploss) :
                self.stoploss = (1-self.stoppercent) * current_price
        # if self.trailing_take_profit:
        #     if (self.takeprofit - current_price) > (self.takeprofit - self.entry_price) * self.stoppercent:
        #         self.takeprofit = (1+self.stoppercent) * current_price
        if self.stoploss is not None and current_price <= self.stoploss:
            return True
        elif self.takeprofit is not None and current_price >= self.takeprofit:
            return True
        return False
    
class SellOrder:
    def __init__(self, entry_price, quantity, stoploss=None, takeprofit=None, traling_stop_loss: bool = False, 
            trailing_take_profit: bool = False, entry_date=None):
        self.entry_date = entry_date
        self.close_date = None
        self.entry_price = entry_price
        self.quantity = quantity
        self.stoppercent = stoploss
        self.trailing_stop_loss = traling_stop_loss
        self.trailing_take_profit = trailing_take_profit
        self.stoploss = (1+stoploss)*entry_price if stoploss is not None else None
        self.takeprofit = (1-takeprofit)*entry_price if takeprofit is not None else None
        self.status = 'open'
        self.type = 'sell'
    def close(self, close_price, close_date=None):
        self.close_date = close_date
        self.close_price = close_price
        self.pl = self.quantity * (self.entry_price - self.close_price)
        self.status = 'closed'
    def check(self, current_price) -> bool:
        if self.trailing_stop_loss:
            if (self.stoploss - current_price) > (self.stoploss - self.entry_price) :
                self.stoploss = (1+self.stoppercent) * current_price
        if self.stoploss is not None and current_price >= self.stoploss:
            return True
        elif self.takeprofit is not None and current_price <= self.takeprofit:
            return True
        return False