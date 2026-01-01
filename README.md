# rohan_binance_bot
A CLI based trading bot made using python
Binance Futures Trading Bot

Author: Rohan Bidkar
Created: January 2026

A professional trading bot for Binance Futures that handles multiple order types with proper logging and validation. Built for educational purposes and safe testnet trading.


WHY THIS BOT?

If you're learning cryptocurrency trading, you need a reliable tool that lets you place orders programmatically without dealing with complex API documentation. This bot simplifies that process while teaching you how real trading automation works.


WHAT CAN IT DO?

Market Orders
Place orders that execute immediately at the current market price. Useful when you want to enter or exit a position quickly.

Limit Orders  
Set a specific price and wait for the market to reach it. More control over your entry and exit prices.

TWAP Orders (Time-Weighted Average Price)
Split a large order into smaller chunks and execute them over time. This strategy helps reduce market impact and often gets better average prices, especially for large trades.


PROJECT STRUCTURE

rohan-binance-bot/
├── src/
│   ├── bot.py                 # Main entry point
│   ├── config.py              # API setup and client
│   ├── market_orders.py       # Market order logic
│   ├── limit_orders.py        # Limit order logic
│   ├── logger.py              # Logging setup
│   ├── advanced/
│   │   ├── twap.py            # TWAP order strategy
│   │   └── __pycache__/
│   └── __pycache__/
├── bot.log                    # Trading activity logs
├── README.md                  # This file
├── requirement.txt            # Dependencies
├── .env                       # Your API keys (keep private)
└── venv/                      # Python environment


WHAT YOU NEED

Python 3.8 or newer
A Binance account (testnet recommended for learning)
Binance API keys (get these from your Binance account)
pip for package management

---

## 📥 Installation & Setup

### Step 1: Clone or Download the Project

```bash
# Clone from GitHub
git clone https://github.com/rohan-bidkar/rohan-binance-bot.git
cd rohan-binance-bot
```

Or extract the ZIP file and navigate to the project directory.

### Step 2: Create Virtual Environment

```powershell
# On Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirement.txt
```

**Expected Output:**
```
Successfully installed python-binance python-dotenv
```

### Step 4: Verify Installation

```bash
python -c "import binance; print(binance.__version__)"
python -c "import dotenv; print('dotenv installed')"
```

---

## ⚙️ Configuration


GETTING STARTED

Step 1: Set up Python Environment

If you haven't already, create a virtual environment to keep dependencies isolated:

  python -m venv venv
  .\venv\Scripts\Activate.ps1       (Windows PowerShell)
  source venv/bin/activate          (Mac/Linux)

Step 2: Install Requirements

  pip install -r requirement.txt

This installs python-binance (the API wrapper) and python-dotenv (for managing API keys).

Step 3: Get Your API Keys

Go to Binance and create API keys:
- For testing: Use Binance Testnet (safe, no real money)
- For live trading: Binance main account (use with care)

Important: Enable "Futures Trading" permission on your API key.
Never share your API secret.

Step 4: Add Your API Keys

Create a file called .env in your project folder:

  BINANCE_API_KEY=your_key_here
  BINANCE_API_SECRET=your_secret_here

That's it. Don't commit this file to GitHub.

Step 5: Test the Connection

  python src/bot.py

You should see help information without any errors.


HOW TO USE IT

The bot uses a simple command format. Here are the basics:

MARKET ORDERS

Execute an order at current price:

  python src/bot.py market -s BTCUSDT -sd BUY -q 0.01

This buys 0.01 BTC at market price. Parameters:
  -s : Trading pair (BTCUSDT, ETHUSDT, etc)
  -sd: BUY or SELL
  -q : Quantity to trade

Example output:
  Symbol: BTCUSDT
  Side: BUY
  Quantity: 0.01
  Order ID: 1234567890
  Status: FILLED


LIMIT ORDERS

Set a specific price and wait:

  python src/bot.py limit -s BTCUSDT -sd BUY -q 0.01 -p 40000

This places a buy order for 0.01 BTC at $40,000. The order sits on the books until your price is reached.

Parameters:
  -s : Trading pair
  -sd: BUY or SELL
  -q : Quantity
  -p : Price you want


TWAP ORDERS (The Interesting One)

Split a big trade into smaller pieces over time:

  python src/bot.py twap -s BTCUSDT -sd BUY -q 1.0 -p 40000 -c 5 -i 60

This splits 1.0 BTC into 5 orders, executing one every 60 seconds.

Parameters:
  -s  : Trading pair
  -sd : BUY or SELL
  -q  : Total quantity
  -p  : Price for each chunk
  -c  : How many chunks to split into
  -i  : Seconds between each order

Pro tip: Use --dry-run first to see the execution plan:

  python src/bot.py twap -s BTCUSDT -sd BUY -q 1.0 -p 40000 -c 5 -i 60 --dry-run

This shows you exactly what will happen without actually placing orders.
Symbol: BTCUSDT
Side: BUY
Total Quantity: 1.0
Price: 40000.0
Number of Chunks: 5
Interval: 60 seconds
Chunk Size: 0.20000000
Remainder: 0.00000000

Execution Schedule:
----------------------------------------------------------------------
Order 1: 0.20000000 BTCUSDT at $40000.0 (+0s from start)
Order 2: 0.20000000 BTCUSDT at $40000.0 (+60s from start)
Order 3: 0.20000000 BTCUSDT at $40000.0 (+120s from start)
Order 4: 0.20000000 BTCUSDT at $40000.0 (+180s from start)
Order 5: 0.20000000 BTCUSDT at $40000.0 (+240s from start)
----------------------------------------------------------------------
Total Execution Time: 240 seconds (~4.0 minutes)
======================================================================
```

**TWAP Live Output (With Execution):**
```
✓ Order 1/5 placed (Order ID: 1234567890)
✓ Order 2/5 placed (Order ID: 1234567891)
✓ Order 3/5 placed (Order ID: 1234567892)
✓ Order 4/5 placed (Order ID: 1234567893)
✓ Order 5/5 placed (Order ID: 1234567894)

======================================================================
TWAP ORDER EXECUTION COMPLETED
======================================================================
Symbol: BTCUSDT
Side: BUY
Total Quantity: 1.00000000
Executed Quantity: 1.00000000
Price: $40000.0
Number of Chunks: 5
Interval: 60 seconds

Order IDs: [1234567890, 1234567891, 1234567892, 1234567893, 1234567894]
Status: completed
======================================================================
```

---

## 📖 Order Types

### Market Orders
- **Use Case:** Execute immediately at best available price
- **Pros:** Fast execution, guaranteed fill
- **Cons:** Price slippage, higher market impact for large orders
- **Example:** Quick position entry/exit

### Limit Orders
- **Use Case:** Execute only at specified price or better
- **Pros:** Better price control, no slippage
- **Cons:** May not fill if price doesn't reach level
- **Example:** Patient buying/selling at target prices

### TWAP (Time-Weighted Average Price)
- **Use Case:** Execute large orders with minimal market impact
- **Pros:** Better average price, reduced slippage, stealth
- **Cons:** Longer execution time, price may move against you
- **Example:** Buying/selling large positions gradually

---

## 📊 Logging

All bot activities are logged to `bot.log` with timestamps, log levels, and detailed messages.

### Log File Location
```
./bot.log
```

### Log Format
```
2026-01-15 10:30:45,123 | INFO | Placing MARKET order | BTCUSDT | BUY | 0.01
2026-01-15 10:30:46,456 | INFO | Market order placed successfully | Order ID: 1234567890
2026-01-15 10:31:02,789 | ERROR | Order failed: Invalid symbol format
```

### Log Levels
- **INFO:** Successful operations, order placements
- **WARNING:** Non-critical issues, partial failures
- **ERROR:** Failed operations, exceptions

### Log Rotation
- **Max File Size:** 5 MB
- **Backup Copies:** 3 previous logs maintained
- **Auto Cleanup:** Old logs automatically compressed

### Viewing Logs

```powershell
# View last 50 lines
tail -n 50 bot.log

# View real-time logs (PowerShell)
Get-Content -Path bot.log -Wait

# Search for errors
Select-String "ERROR" bot.log
```

---

## 🔌 API Reference

### Module: `market_orders.py`

```python
def validate_inputs(symbol: str, side: str, quantity: float) -> None
    """Validate market order inputs"""

def place_market_order(symbol: str, side: str, quantity: float) -> dict
    """Execute a market order"""
```

### Module: `limit_orders.py`

```python
def validate_inputs(symbol: str, side: str, quantity: float, price: float) -> None
    """Validate limit order inputs"""

def place_limit_order(symbol: str, side: str, quantity: float, price: float) -> dict
    """Execute a limit order"""
```

### Module: `advanced/twap.py`

```python
def validate_twap_inputs(...) -> None
    """Validate TWAP order parameters"""

def place_twap_order(symbol: str, side: str, total_quantity: float, 
                     price: float, num_chunks: int, interval_seconds: int, 
                     dry_run: bool = False) -> dict
    """Execute TWAP orders"""
```

---

## ❌ Troubleshooting

### Issue: "API Key and Secret must be set in the .env file"

**Solution:**
1. Create `.env` file in project root
2. Add `BINANCE_API_KEY` and `BINANCE_API_SECRET`
3. Save and restart bot

```bash
# Verify .env file exists
ls -la .env
```

---

### Issue: "Invalid symbol format"

**Solution:**
Symbols must be in uppercase without special characters:
```bash
# ❌ Wrong
python src/bot.py market -s btcusdt -sd BUY -q 0.01
python src/bot.py market -s BTC-USDT -sd BUY -q 0.01

# ✅ Correct
python src/bot.py market -s BTCUSDT -sd BUY -q 0.01
```

---

### Issue: "Quantity must be greater than 0"

**Solution:**
Ensure quantity is a positive number:
```bash
# ❌ Wrong
python src/bot.py market -s BTCUSDT -sd BUY -q 0
python src/bot.py market -s BTCUSDT -sd BUY -q -0.01

# ✅ Correct
python src/bot.py market -s BTCUSDT -sd BUY -q 0.01
```

---

### Issue: "Side must be BUY or SELL"

**Solution:**
Use only BUY or SELL (case-insensitive):
```bash
# ❌ Wrong
python src/bot.py market -s BTCUSDT -sd buy -q 0.01

# ✅ Correct
python src/bot.py market -s BTCUSDT -sd BUY -q 0.01
```

---

### Issue: Connection timeout or API errors

**Solution:**
1. Check internet connection
2. Verify API credentials
3. Check Binance API status
4. Check logs: `cat bot.log`

```bash
# Test connection
python -c "from config import client; print('Connected!')"
```

---

### Issue: "Chunks cannot exceed total quantity"

**Solution:**
Number of chunks must not exceed total quantity:
```bash
# ❌ Wrong: 5 chunks but only 1.0 total (old validation - now fixed)

# ✅ Correct
python src/bot.py twap -s BTCUSDT -sd BUY -q 1.0 -p 40000 -c 5 -i 60
```

---

##  Future Enhancements

### Short-term (Next Release)
- [ ] Stop-Limit Orders (price trigger + limit execution)
- [ ] Grid Orders (automated buy-low/sell-high)
- [ ] OCO Orders (One-Cancels-Other)
- [ ] Order cancellation commands
- [ ] Position monitoring

### Medium-term
- [ ] Web dashboard for order monitoring
- [ ] Strategy backtesting engine
- [ ] Integration with Fear & Greed Index
- [ ] Automated risk management
- [ ] Multi-account support

### Long-term
- [ ] Machine learning for price prediction
- [ ] Advanced charting & technical analysis
- [ ] REST API server
- [ ] Desktop GUI application

---

## 📝 Example Trading Scenarios

### Scenario 1: Conservative Entry with Limit Orders

```bash
# Strategy: Buy at target price only
python src/bot.py limit -s BTCUSDT -sd BUY -q 0.1 -p 38000
python src/bot.py limit -s BTCUSDT -sd BUY -q 0.1 -p 39000
python src/bot.py limit -s BTCUSDT -sd BUY -q 0.1 -p 40000
```

**Result:** Three orders queued. Execute only if prices drop to your targets.

---

### Scenario 2: Aggressive Entry with Market Order

```bash
# Strategy: Enter immediately
python src/bot.py market -s BTCUSDT -sd BUY -q 0.3
```

**Result:** Buy 0.3 BTC at current market price instantly.

---

### Scenario 3: Stealth Large Position with TWAP

```bash
# Strategy: Execute large order without price impact
python src/bot.py twap -s BTCUSDT -sd BUY -q 1.0 -p 40000 -c 10 -i 30

# Preview first
python src/bot.py twap -s BTCUSDT -sd BUY -q 1.0 -p 40000 -c 10 -i 30 --dry-run
```

**Result:** Buy 1.0 BTC gradually (0.1 BTC every 30 seconds) over 5 minutes.

---

Support & Contact

**Author:** Rohan Bidkar  
**GitHub:** [rohan-bidkar](https://github.com/rohan-bidkar)  
**Project:** rohan-binance-bot

For issues, questions, or suggestions:
1. Check the Troubleshooting section
2. Review bot.log for error details
3. Check [Binance API Docs](https://binance-docs.github.io/apidocs/futures/en/)

---

