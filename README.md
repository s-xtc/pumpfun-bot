# **PumpFun Automated Trading System**

This script automates cryptocurrency trading through a WebSocket interface, allowing for auto-buy and auto-sell functionality. It can be configured to monitor the market for new tokens and perform automated trades based on predefined rules.

## **Features**
- Auto-buy new tokens based on market conditions.
- Auto-sell tokens when a profit/loss threshold is reached.
- Real-time monitoring of the market via WebSocket.
- Configurable slippage, priority fee, and other settings for trades.


## **Requirements**
- Python 3.8+
- `requests` library
- `websockets` library
- `rich` library (for pretty-printing)
- Internet connection for API communication and WebSocket data

## **Installation**

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/s-xtc/pumpfun-bot.git
   cd pumpfun-bot
   ```

2. Install the required libraries using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

## **Configuration**

Before running the script, you need to configure it with your API key and other settings.

1. Open the script `trader.py` and update the following configuration values in the `config` dictionary:

   - `API_KEY`: Replace `"api-key"` with your actual API key.
   - `TRADE_URL`: URL for making trade requests (usually provided by your trading API).
   - `WS_URI`: WebSocket URI for receiving market data.
   - `AUTO_BUY_AMOUNT_SOL`: The amount of SOL to use when buying tokens.
   - `AUTO_SELL_WIN_PERCENT`: The percentage gain to trigger a sell action.
   - `AUTO_SELL_LOSS_PERCENT`: The percentage loss to trigger a sell action.
   - `AUTO_SELL_TIME_LIMIT`: Time limit (in seconds) for auto-sell.
   - `SLIPPAGE`: Maximum slippage allowed when making trades.
   - `PRIORITY_FEE`: Additional priority fee for transactions (if applicable).

## **Running the Script**

To start the script, execute the following command:

```bash
python trader.py
```

Upon running the script, you will be prompted with the following menu:

```
PumpFun Automated Trading System
1. Start market monitoring with auto-buy and auto-sell
3. Exit
```

### **Menu Options**
1. **Start market monitoring**  
   This option will begin the process of monitoring the market for new tokens and execute auto-buy and auto-sell trades based on the settings configured earlier.

2. **Exit**  
   This will stop the program and exit the script.

## **How It Works**
- **Market Monitoring:**  
   The script connects to a WebSocket (defined by `WS_URI`) and subscribes to notifications for new tokens. When a new token is detected, the script automatically buys it using the amount specified in `AUTO_BUY_AMOUNT_SOL`.
  
- **Auto-Sell:**  
   After a successful buy, the script monitors the price of the token. It will automatically sell if:
   - The price reaches a certain profit threshold (defined by `AUTO_SELL_WIN_PERCENT`).
   - The price drops to a certain loss threshold (defined by `AUTO_SELL_LOSS_PERCENT`).
   - The time limit (defined by `AUTO_SELL_TIME_LIMIT`) expires.
   
- **Trade Execution:**  
   The script uses the `requests` library to make HTTP requests to the trade API with the necessary payload, which includes trade action (buy/sell), token mint address, amount, slippage, and priority fee.

## **Customization**

You can customize various settings in the `config` dictionary such as:
- Amount of SOL used for auto-buy (`AUTO_BUY_AMOUNT_SOL`).
- The percentage at which to sell for profit or loss (`AUTO_SELL_WIN_PERCENT`, `AUTO_SELL_LOSS_PERCENT`).
- Time limit for auto-sell (`AUTO_SELL_TIME_LIMIT`).
- Slippage tolerance (`SLIPPAGE`).
- API key and trade URL.

## **Error Handling**

If there is an issue with executing a trade (e.g., invalid API key, network issue), the script will display an error message.

---

For further customization or troubleshooting, refer to the comments in the code or contact support.
If you want to donate my sol adress is: G1SJckY7NqiMYvDWLPDQu9z84QtueZjD6qDPASAux21r
