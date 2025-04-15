from typing import List, Union
from backtesting.order_class import BuyOrder, SellOrder
import logging


class Positions:
    def __init__(self, initial_capital: float, leverage: float = 1, transaction_fee_rate: float = 0.005, traling_stop_loss: bool = False, trailing_take_profit: bool = False) -> None:
        self.positions: List[Union[BuyOrder, SellOrder]] = []
        self.closed_positions: List[Union[BuyOrder, SellOrder]] = []
        self.leverage: float = leverage
        self.profit: float = 0
        self.loss: float = 0
        self.profit_loss: float = 0
        self.profit_count: int = 0
        self.loss_count: int = 0
        self.initial_capital: float = initial_capital
        self.current_capital: float = initial_capital
        self.available_capital: float = initial_capital* leverage
        self.transaction_fee_rate: float = transaction_fee_rate 
        self.traling_stop_loss: bool = traling_stop_loss
        self.trailing_take_profit: bool = trailing_take_profit
        self.capital_history: List[float] = []
        self.available_capital_history: List[float] = []

        

    def add_position(self, position: Union[BuyOrder, SellOrder]) -> None:
        position_cost = position.entry_price * position.quantity
        transaction_fee = position_cost * self.transaction_fee_rate

        if isinstance(position, BuyOrder) and self.available_capital >= (position_cost + transaction_fee):
            self.available_capital -= (position_cost + transaction_fee)
            self.profit_loss -= transaction_fee
            self.current_capital -= transaction_fee
            self.positions.append(position)
        elif isinstance(position, SellOrder) and self.available_capital >= (position_cost + transaction_fee):
            self.available_capital -= (position_cost + transaction_fee)
            self.profit_loss -= transaction_fee
            self.current_capital -= transaction_fee 
            self.positions.append(position)
        else:
            logging.warning(f"Skipping position due to insufficient funds: {position}")

    def check_positions(self, current_price: float, date: str) -> None:
        for position in self.positions[:]:  
            if position.check(current_price):
                self.close_position(position, current_price, date)
        self.capital_history.append(self.current_capital)
        self.available_capital_history.append(self.available_capital)

    def close_position(self, position: Union[BuyOrder, SellOrder], close_price: float, date: str) -> None:
        position.close(close_price, date)

        self.profit_loss += position.pl

        if isinstance(position, BuyOrder):
            self.current_capital += position.pl
            self.available_capital += (position.quantity * close_price)
        elif isinstance(position, SellOrder):
            self.current_capital += position.pl
            self.available_capital += (position.quantity * close_price) + 2*position.pl

        if position.pl > 0:
            self.profit_count += 1
            self.profit += position.pl
        else:
            self.loss_count += 1
            self.loss += position.pl


        self.closed_positions.append(position)
        self.positions.remove(position)


    def close_all_positions(self, close_price: float, date: str) -> None:
        for position in self.positions[:]: 
            self.close_position(position, close_price, date)

    def get_positions(self) -> List[Union[BuyOrder, SellOrder]]:
        return self.positions

    def get_closed_positions(self) -> List[Union[BuyOrder, SellOrder]]:
        return self.closed_positions

    def get_profit_loss(self) -> float:
        return self.profit_loss

    def get_success_rate(self) -> float:
        total_trades = self.profit_count + self.loss_count
        return self.profit_count / total_trades if total_trades > 0 else 0

    def get_profit_count(self) -> int:
        return self.profit_count

    def get_loss_count(self) -> int:
        return self.loss_count

    def get_current_capital(self) -> float:
        return self.current_capital

    def get_total_value(self) -> float:
        open_positions_value = sum(p.quantity * p.price for p in self.positions)
        return self.current_capital + open_positions_value
    
    def get_capital_history(self) -> List[float]:
        return self.capital_history
    
    def get_available_capital_history(self) -> float:
        return self.available_capital_history
    
    def get_profit_factor(self) -> float:
        return abs(self.profit / self.loss) if self.loss != 0 else float('inf')

    def get_max_drawdown(self) -> float:
        max_drawdown = 0
        peak = self.capital_history[0]
        for capital in self.capital_history:
            if capital > peak:
                peak = capital
            drawdown = (peak - capital) / peak
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        return max_drawdown
    
    