import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
from typing import List
from backtesting.positions import Positions
from backtesting.order_class import BuyOrder, SellOrder
import numpy as np
from tqdm import tqdm 
import sys
import random

class Backtest:
    def __init__(self, data: pd.DataFrame, signals: List, price_column: str = "close", date_column: str = "date", BUY_SIGNAL=0, SELL_SIGNAL=2):
        """
        Initialize the Backtest class with data and signals.
        """
        self.data = data
        self.signals = signals
        self.price_column = price_column
        self.date_column = date_column
        self.BUY_SIGNAL = BUY_SIGNAL
        self.SELL_SIGNAL = SELL_SIGNAL

    def _validate_inputs(self, stop_loss, take_profit, transaction_fee_rate, initial_capital, quantity):
        """
        Validate the input parameters and data.
        """
        if self.price_column not in self.data.columns:
            raise ValueError(f"Price column '{self.price_column}' not found in data.")
        if self.date_column not in self.data.columns:
            raise ValueError(f"Date column '{self.date_column}' not found in data.")
        if len(self.data) == 0:
            raise ValueError("Data is empty.")
        if len(self.signals) == 0:
            raise ValueError("Signals are empty.")
        if len(self.data) != len(self.signals):
            raise ValueError("Data and signals must have the same length.")
        if initial_capital <= 0:
            raise ValueError("Initial capital must be a positive number.")
        if quantity <= 0:
            raise ValueError("Quantity must be a positive number.")
        if stop_loss < 0 or stop_loss > 1:
            raise ValueError("Stop loss must be between 0 and 1.")
        if take_profit < 0 or take_profit > 1:
            raise ValueError("Take profit must be between 0 and 1.")
        if transaction_fee_rate < 0 or transaction_fee_rate > 1:
            raise ValueError("Transaction fee rate must be between 0 and 1.")
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("Data must be a pandas DataFrame.")

    def _filter_data(self, start_date: str = None, end_date: str = None, last_n: int = None):
        """
        Filter the data based on date range or the last N rows.
        """
        if last_n is not None:
            if last_n <= 0:
                raise ValueError("last_n must be a positive integer.")
            if last_n > len(self.data):
                raise ValueError("last_n exceeds the length of the data.")
            self.data = self.data.iloc[-last_n:]
            self.signals = self.signals[-last_n:]
        else:
            if start_date is not None:
                mask = self.data[self.date_column] >= start_date
                self.data = self.data[mask]
                self.signals = [signal for signal, valid in zip(self.signals, mask) if valid]
            if end_date is not None:
                mask = self.data[self.date_column] <= end_date
                self.data = self.data[mask]
                self.signals = [signal for signal, valid in zip(self.signals, mask) if valid]

    def _initialize_positions(self, initial_capital, leverage, transaction_fee_rate, trailing_take_profit, traling_stop_loss):
        """
        Initialize the Positions object.
        """
        return Positions(
            initial_capital,
            leverage=leverage,
            transaction_fee_rate=transaction_fee_rate,
            trailing_take_profit=trailing_take_profit,
            traling_stop_loss=traling_stop_loss
        )

    def _execute_trades(self, positions, prices, dates, stop_loss, take_profit, quantity, dynamic_position_size: bool = False, risk_per_trade: float = 0.01, leverage: float = 1, max_slippage: float = 0.00):  
        """
        Execute trades based on signals and update positions.
        """
        def calculate_dynamic_position_size(price):
            q = float(positions.current_capital * leverage* risk_per_trade)/float(price)
            return q
        if dynamic_position_size:
            print("Dynamic Position Size: ON")
            for i in tqdm(range(len(prices)), desc="Executing Trades", unit="trade", file=sys.stdout):
                price = prices[i]
                signal = self.signals[i]
                date = dates[i]
                positions.check_positions(price, date)

                if signal == self.BUY_SIGNAL:  # Buy signal
                    try:
                        quantity = calculate_dynamic_position_size(price)
                        buy_order = BuyOrder(
                            entry_price=price + max_slippage*price*(random.uniform(-1, 1)),
                            quantity=quantity,
                            stoploss=stop_loss,
                            takeprofit=take_profit,
                            traling_stop_loss=positions.traling_stop_loss,
                            trailing_take_profit=positions.trailing_take_profit,
                            entry_date=date
                        )
                        positions.add_position(buy_order)
                    except ValueError:
                        pass  # Insufficient capital, skip this trade
                elif signal == self.SELL_SIGNAL:  # Sell signal
                    quantity = calculate_dynamic_position_size(price)
                    sell_order = SellOrder(
                        entry_price=price+ max_slippage*price*(random.uniform(-1, 1)),
                        quantity=quantity,
                        stoploss=stop_loss,
                        takeprofit=take_profit,
                        traling_stop_loss=positions.traling_stop_loss,
                        trailing_take_profit=positions.trailing_take_profit,
                        entry_date=date
                    )
                    positions.add_position(sell_order)


        else:
            print("Dynamic Position Size: OFF")
            for i in tqdm(range(len(prices)), desc="Executing Trades", unit="trade", file=sys.stdout):
                price = prices[i]
                signal = self.signals[i]
                date = dates[i]
                positions.check_positions(price, date)

                if signal == self.BUY_SIGNAL:  # Buy signal
                    try:
                        
                        buy_order = BuyOrder(
                            entry_price=price,
                            quantity=quantity,
                            stoploss=stop_loss,
                            takeprofit=take_profit,
                            traling_stop_loss=positions.traling_stop_loss,
                            trailing_take_profit=positions.trailing_take_profit,
                            entry_date=date
                        )
                        positions.add_position(buy_order)
                    except ValueError:
                        pass  # Insufficient capital, skip this trade
                elif signal == self.SELL_SIGNAL:  # Sell signal
                    sell_order = SellOrder(
                        entry_price=price,
                        quantity=quantity,
                        stoploss=stop_loss,
                        takeprofit=take_profit,
                        traling_stop_loss=positions.traling_stop_loss,
                        trailing_take_profit=positions.trailing_take_profit,
                        entry_date=date
                    )
                    positions.add_position(sell_order)


    def _generate_results(self, positions, initial_capital):
        """
        Generate and return the backtest results.
        """
        total_trades = positions.get_profit_count() + positions.get_loss_count()
        win_rate = positions.get_success_rate()
        profit_loss = positions.get_profit_loss()
        final_capital = positions.get_current_capital()
        profit_factor = positions.get_profit_factor()
        max_drawdown = positions.get_max_drawdown()
        total_return = (final_capital - initial_capital) / initial_capital * 100

        results = {
            "Total Trades": total_trades,
            "Win Rate (%)": f"{win_rate:.2f}",
            "Profit Factor": f"{profit_factor:.2f}",
            "Max Drawdown (%)": f"{max_drawdown:.2f}",
            "Profit/Loss": f"${profit_loss:.2f}",
            "Initial Capital": f"${initial_capital:,.2f}",
            "Final Capital": f"${final_capital:,.2f}",
            "Return (%)": f"{total_return:.2f}%"
        }
        return results

    def _plot_results(self, prices, positions):
        """
        Plot the backtest results.
        """

        self.data[self.date_column] = pd.to_datetime(self.data[self.date_column])

        # Create backtest results DataFrame
        equity_curve = positions.get_capital_history()
        available_capital = positions.get_available_capital_history()
        drawdown = positions.get_max_drawdown()
        backtest_results = pd.DataFrame({
            "Price": prices,
            "date": self.data[self.date_column],
            "equity_curve": equity_curve,
            "drawdown": drawdown,
            "available_capital": available_capital
        })

        plt.figure(figsize=(14, 10))

        # Price and Signals Plot
        plt.subplot(5, 1, 1)
        plt.plot(self.data[self.date_column], prices, label='Price', color='navy')
        buy_signals = np.where(self.signals == np.int64(self.BUY_SIGNAL))[0]
        sell_signals = np.where(self.signals == np.int64(self.SELL_SIGNAL))[0]
        plt.scatter(self.data[self.date_column].iloc[buy_signals], prices[buy_signals], marker='^', color='lime', s=100, label='Buy Signal')
        plt.scatter(self.data[self.date_column].iloc[sell_signals], prices[sell_signals], marker='v', color='red', s=100, label='Sell Signal')
        plt.title('Price Action with Trading Signals')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)

        # Format x-axis for better readability
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())  # Automatically adjust the number of ticks
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates as 'YYYY-MM-DD'
        plt.xticks(rotation=45)  # Rotate x-axis labels

        # Equity Curve Plot
        plt.subplot(5, 1, 2)
        sns.lineplot(data=backtest_results, x="date", y="equity_curve", color="blue")
        plt.title("Equity Curve")
        plt.xlabel("Date")
        plt.ylabel("Portfolio Value")
        plt.grid(True)

        #Available Capital Plot
        plt.subplot(5, 1, 3)
        sns.lineplot(data=backtest_results, x="date", y="available_capital", color="blue")
        plt.title("Available Capital")
        plt.xlabel("Date")
        plt.ylabel("Available Capital")
        plt.grid(True)
        plt.fill_between(backtest_results['date'], backtest_results['available_capital'], color='blue', alpha=0.3)
        

        # Format x-axis for better readability
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)

        # Drawdown Plot
        plt.subplot(5, 1, 4)
        sns.lineplot(data=backtest_results, x="date", y="drawdown", color="red")
        plt.fill_between(backtest_results['date'], backtest_results['drawdown'], color='red', alpha=0.3)
        plt.title("Drawdown Over Time")
        plt.xlabel("Date")
        plt.ylabel("Drawdown (%)")
        plt.grid(True)

        # Format x-axis for better readability
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)

        # Win/Loss Distribution
        plt.subplot(5, 1, 5)
        total_trades = positions.get_profit_count() + positions.get_loss_count()
        if total_trades > 0:
            labels = ['Profitable Trades', 'Losing Trades']
            sizes = [positions.get_profit_count(), positions.get_loss_count()]
            colors = ['#66b3ff', '#ff9999']
            plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, explode=(0.1, 0), shadow=True)
            plt.title('Trade Performance Distribution')
        else:
            plt.text(0.5, 0.5, 'No Trades Executed', ha='center', va='center')

        plt.tight_layout()
        plt.show()
    def run(self, stop_loss: float, take_profit: float, initial_capital: float = 10000, leverage: float = 1, quantity: int = 1,
            last_n: int = None, transaction_fee_rate: float = 0.002, traling_stop_loss: bool = False,
            trailing_take_profit: bool = False, start_date: str = None, end_date: str = None, plot: bool = True,
            dynamic_position_size: bool = False, risk_per_trade: float = 0.01, max_slippage: float = 0.00):
        """
        Run the backtest.
        """
        self._validate_inputs(stop_loss, take_profit, transaction_fee_rate, initial_capital, quantity)
        self._filter_data(start_date, end_date, last_n)

        prices = self.data[self.price_column].values
        dates = self.data[self.date_column].values
        self.positions = self._initialize_positions(initial_capital, leverage, transaction_fee_rate, trailing_take_profit, traling_stop_loss)

        # Execute trades
        self._execute_trades(self.positions, prices, dates, stop_loss, take_profit, quantity, dynamic_position_size, risk_per_trade, leverage, max_slippage)

        results = self._generate_results(self.positions, initial_capital)

        # Print results
        print("BACKTEST RESULT :\n")
        print(pd.DataFrame.from_dict(results, orient='index').to_markdown(tablefmt="grid"))

        # Plot results
        if plot:
            self._plot_results(prices, self.positions)

        return results
    
    def get_positions(self):
        """"
        "Get the current positions.
        """
        return self.positions.get_positions()
    def get_closed_positions(self):
        """
        Get the closed positions.
        """
        return self.positions.get_closed_positions()
    def print_closed_positions(self, n: int = None):
        """
        Print the closed positions in a table format.
        
        Args:
            n (int, optional): Number of positions to print. If None, prints all positions.
        """
        closed_positions = self.positions.get_closed_positions()
        
        if not closed_positions:
            print("No closed positions.")
            return
        
        trade_data = []
        for pos in closed_positions:
            position_type = "BUY" if isinstance(pos, BuyOrder) else "SELL"
            trade_data.append({
                'Type': position_type,
                'Entry Date': pos.entry_date,
                'Exit Date': pos.close_date,
                'Entry Price': f"${pos.entry_price:.2f}",
                'Exit Price': f"${pos.close_price:.2f}",
                'Quantity': pos.quantity,
                'P/L': f"${pos.pl:.2f}",
                'P/L %': f"{(pos.pl / (pos.entry_price * pos.quantity)) * 100:.2f}%",
                'Duration': pd.to_datetime(pos.close_date) - pd.to_datetime(pos.entry_date)
            })
        
        # Convert to DataFrame for nice display
        df = pd.DataFrame(trade_data)
        
        # Limit rows if specified
        if n is not None and n > 0:
            df = df.tail(n)
        
        # Sort by exit date (most recent first)
        df = df.sort_values('Exit Date', ascending=False)
        
        # Print table
        print("\n📊 CLOSED POSITIONS SUMMARY")
        print("=" * 80)
        print(df.to_markdown(tablefmt="grid", index=False))
        
        # Print summary statistics
        profitable_trades = sum(1 for pos in closed_positions if pos.pl > 0)
        total_trades = len(closed_positions)
        win_rate = profitable_trades / total_trades * 100 if total_trades > 0 else 0
        total_pl = sum(pos.pl for pos in closed_positions)
        
        print("\n📈 SUMMARY STATISTICS")
        print("=" * 80)
        print(f"Total Trades: {total_trades}")
        print(f"Profitable Trades: {profitable_trades}")
        print(f"Win Rate: {win_rate:.2f}%")
        print(f"Total P/L: ${total_pl:.2f}")
    