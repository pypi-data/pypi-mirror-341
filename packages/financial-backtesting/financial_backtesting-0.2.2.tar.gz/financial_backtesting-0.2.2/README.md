# Financial Backtesting

A Python library for backtesting financial trading strategies using machine learning models and custom signals. This library provides a robust framework for simulating trades, analyzing performance, and visualizing results.

---

## Features

- **Dynamic Position Sizing**: Supports risk-based position sizing for better capital management.
- **Customizable Parameters**: Configure stop-loss, take-profit, leverage, transaction fees, and more.
- **Comprehensive Metrics**: Provides detailed performance metrics such as win rate, profit factor, drawdown, and total return.
- **Visualization**: Generates plots for equity curves, drawdowns, and trade signals.
- **Trade Logging**: Tracks and summarizes closed positions for detailed analysis.

---

## Installation

Install the package using pip:

```bash
pip install financial-backtesting
```

---

## Usage

### 1. **Import the Library**

```python
from backtesting import Backtest
```

### 2. **Prepare Your Data**

Ensure your data is a `pandas.DataFrame` with at least the following columns:
- **Price Column**: The column containing price data (e.g., `close`).
- **Date Column**: The column containing date/time data (e.g., `date`).
- **Signals**: A list or array of buy/sell signals.

### 3. **Run a Backtest**

```python
# Example DataFrame
import pandas as pd
df = pd.read_csv("your_data.csv")

# Example signals (0 = Buy, 2 = Sell)
signals = [0, 2, 0, 2, ...]

# Initialize the backtest
backtest = Backtest(
    data=df,
    signals=signals,
    price_column="close",
    date_column="date",
    BUY_SIGNAL=0,
    SELL_SIGNAL=2
)

# Run the backtest
results = backtest.run(
    stop_loss=0.01,  # 1% stop loss
    take_profit=0.03,  # 3% take profit
    initial_capital=10000,
    leverage=2,
    quantity=1,
    transaction_fee_rate=0.001,
    dynamic_position_size=True,
    risk_per_trade=0.02,
    max_slippage=0.001,
    plot=True
)

# Print results
print(results)
```

---

## API Reference

### `Backtest` Class

#### **Initialization**
```python
Backtest(data, signals, price_column="close", date_column="date", BUY_SIGNAL=0, SELL_SIGNAL=2)
```
- **data**: `pd.DataFrame` - The input data containing price and date columns.
- **signals**: `List` - A list of buy/sell signals.
- **price_column**: `str` - The column name for price data.
- **date_column**: `str` - The column name for date/time data.
- **BUY_SIGNAL**: `int` - The value representing a buy signal.
- **SELL_SIGNAL**: `int` - The value representing a sell signal.

#### **Methods**
1. **`run()`**
   Runs the backtest with the specified parameters.
   ```python
   run(
       stop_loss: float,
       take_profit: float,
       initial_capital: float = 10000,
       leverage: float = 1,
       quantity: int = 1,
       transaction_fee_rate: float = 0.002,
       dynamic_position_size: bool = False,
       risk_per_trade: float = 0.01,
       max_slippage: float = 0.00,
       start_date: str = None,
       end_date: str = None,
       plot: bool = True
   )
   ```
   - **stop_loss**: Stop-loss percentage (e.g., `0.01` for 1%).
   - **take_profit**: Take-profit percentage (e.g., `0.03` for 3%).
   - **initial_capital**: Starting capital for the backtest.
   - **leverage**: Leverage multiplier.
   - **quantity**: Fixed quantity per trade (ignored if `dynamic_position_size=True`).
   - **transaction_fee_rate**: Transaction fee rate (e.g., `0.001` for 0.1%).
   - **dynamic_position_size**: Whether to use risk-based position sizing.
   - **risk_per_trade**: Risk percentage per trade (used if `dynamic_position_size=True`).
   - **max_slippage**: Maximum slippage percentage.
   - **start_date**: Start date for filtering data.
   - **end_date**: End date for filtering data.
   - **plot**: Whether to generate plots.

2. **`get_positions()`**
   Returns the current open positions.

3. **`get_closed_positions()`**
   Returns the closed positions.

4. **`print_closed_positions(n: int = None)`**
   Prints a summary of closed positions.

---

## Outputs

### Backtest Results
The `run()` method returns a dictionary with the following metrics:
- **Total Trades**: Total number of trades executed.
- **Win Rate (%)**: Percentage of profitable trades.
- **Profit Factor**: Ratio of gross profit to gross loss.
- **Max Drawdown (%)**: Maximum drawdown during the backtest.
- **Profit/Loss**: Total profit or loss in dollars.
- **Initial Capital**: Starting capital.
- **Final Capital**: Ending capital.
- **Return (%)**: Total return percentage.

### Plots
- **Price Action with Signals**: Shows buy/sell signals on the price chart.
- **Equity Curve**: Portfolio value over time.
- **Available Capital**: Remaining capital over time.
- **Drawdown**: Drawdown percentage over time.
- **Trade Performance Distribution**: Pie chart of profitable vs. losing trades.

---

## Example Output

### Backtest Results
```plaintext
+-------------------+----------------+
| Metric            | Value          |
+-------------------+----------------+
| Total Trades      | 50             |
| Win Rate (%)      | 60.00          |
| Profit Factor     | 1.50           |
| Max Drawdown (%)  | -10.00         |
| Profit/Loss       | $1,500.00      |
| Initial Capital   | $10,000.00     |
| Final Capital     | $11,500.00     |
| Return (%)        | 15.00%         |
+-------------------+----------------+
```

### Plots
- **Price Action with Signals**: Shows buy/sell signals on the price chart.
- **Equity Curve**: Portfolio value over time.
- **Drawdown**: Drawdown percentage over time.

---

## Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository and submit a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contact

For questions or feedback, contact **Shashwat Chaturvedi** at [chaturvedishashwat5@gmail.com](mailto:chaturvedishashwat5@gmail.com).
