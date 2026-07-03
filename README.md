# 🤖 Binance Futures Testnet Trading Bot

A Python-based trading bot for placing orders on Binance Futures Testnet (USDT-M) with a clean, reusable structure, proper logging, and enhanced CLI interface.

## ⚠️ Important Notice

This bot is designed for **TESTNET only**. No real money is involved. Always test on testnet before using any trading software with real funds.

## 📋 Features

### Core Requirements ✅
- ✅Place **Market** and **Limit** orders on Binance Futures Testnet
- ✅ Support both **BUY** and **SELL** sides
- ✅ Enhanced CLI with interactive menu mode
- ✅ Input validation with detailed error messages
- ✅ Structured code with separate modules (client, orders, validators, CLI)
- ✅ Comprehensive logging to file and console
- ✅ Exception handling for invalid input, API errors, and network failures
- ✅ Clear order request summaries and execution details

### Enhanced Features 🎁
- ✅ **Interactive CLI Mode**: User-friendly menu system with Rich terminal UI
- ✅ **Validation**: Symbol format validation and price/quantity precision checking
- ✅ **Additional Order Types**: Support for STOP_MARKET orders
- ✅ **Balance Checking**: View account balance for any asset
- ✅ **Order Status**: Check status of existing orders
- ✅ **Order Cancellation**: Cancel pending orders
- ✅ **Colored Output**: Beautiful console output with colorama and Rich
- ✅ **Both CLI modes**: Interactive menu and command-line arguments via Typer

## 🚀 Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Binance Futures Testnet account

### Installation

1. **Clone or download the repository**

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root directory:
   ```env
   BINANCE_API_KEY=your_testnet_api_key_here
   BINANCE_API_SECRET=your_testnet_api_secret_here
   ```

5. **Verify installation**
   ```bash
   python -m trading_bot.cli --help
   ```

## 📖 Usage

### Mode 1: Interactive Menu (Recommended)

Run the bot in interactive mode with a user-friendly menu:

```bash
python trading_bot/cli.py
```

Or explicitly:
```bash
python trading_bot/cli.py menu
```

**Menu Options:**
1. 📊 Check Account Balance
2. 🛒 Place Market Order
3. 📝 Place Limit Order
4. 🔍 Check Order Status
5. ❌ Cancel Order
6. ❌ Exit

### Mode 2: Command Line

Place orders directly via command-line arguments:

**Market Order:**
```bash
python trading_bot/cli.py place-order BTCUSDT BUY MARKET 0.001
```

**Limit Order:**
```bash
python trading_bot/cli.py place-order BTCUSDT SELL LIMIT 0.001 --price 50000
```

**Limit Order with IOC (Immediate or Cancel):**
```bash
python trading_bot/cli.py place-order ETHUSDT BUY LIMIT 0.1 --price 3000 --tif IOC
```

**Show balance after order:**
```bash
python trading_bot/cli.py place-order BTCUSDT BUY MARKET 0.001 --balance
```

**Check Order Status:**
```bash
python trading_bot/cli.py status BTCUSDT 12345
```

**Cancel Order:**
```bash
python trading_bot/cli.py cancel BTCUSDT 12345
```

**Check Balance:**
```bash
python trading_bot/cli.py balance
python trading_bot/cli.py balance --asset BTC
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `BINANCE_API_KEY` | Your Binance Futures Testnet API key | Yes |
| `BINANCE_API_SECRET` | Your Binance Futures Testnet API secret | Yes |

### Logging

Logs are automatically saved to:
- **File**: `logs/trading_bot.log` (rotating log, 10 MB max, 5 backups)
- **Console**: Colored output using Rich

Adjust log level in `logging_config.py`:
```python
setup_logging(log_level="DEBUG")  # or INFO, WARNING, ERROR
```

## 📁 Project Structure

```
trading_bot/
├── trading_bot/
│   ├── __init__.py
│   ├── bot/
│   │   ├── __init__.py
│   │   ├── client.py          # Binance API client wrapper
│   │   ├── orders.py          # Order management and display
│   │   └── validators.py      # Input validation logic
│   ├── logging_config.py      # Logging setup
│   └── cli.py                 # CLI entry point (Typer + Rich)
├── requirements.txt
├── .env                       # Environment variables (create this)
├── .env.example               # Environment variables template
└── README.md
```

## 🔨 How It Works

### Architecture

1. **CLI Layer** (`cli.py`): Handles user input via Typer commands and interactive prompts
2. **Order Manager** (`orders.py`): Business logic, validation orchestration, and display formatting
3. **Binance Client** (`client.py`): Direct API interaction with Binance Futures Testnet
4. **Validators** (`validators.py`): Input validation and business rule enforcement
5. **Logging** (`logging_config.py`): Centralized logging configuration

### Order Flow

```
User Input → Validator → Order Manager → Binance Client → API Response → Display
                ↓              ↓            ↓
            Error Messages   Logging    Error Handling
```

## ✅ Examples

### Example 1: Market Buy Order (Interactive)
```bash
$ python trading_bot/cli.py

╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║     🤖  Binance Futures Testnet Trading Bot  🤖              ║
║                                                               ║
║          Trade safely on the Binance Testnet                 ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

⚠️  This is for TESTNET only. No real money involved.

Main Menu:
  1. Check Account Balance
  2. Place Market Order
  3. Place Limit Order
  4. Check Order Status
  5. Cancel Order
  6. Exit

Select option: 2

Placing MARKET Order
Enter symbol: BTCUSDT
Enter side: BUY
Enter quantity: 0.001

Order Summary:
  BUY 0.001 BTCUSDT @ MARKET

Confirm order?: Yes

============================================================
✓ ORDER PLACED SUCCESSFULLY
============================================================

Order Details:
  Symbol:          BTCUSDT
  Side:            BUY
  Type:            MARKET
  Quantity:        0.001

Execution Details:
  Order ID:        12345
  Status:          FILLED
  Executed Qty:    0.001
  Avg Price:       50000.0
  Cumulative Quote:50.0
  Timestamp:       2024-01-15T12:34:56
============================================================
```

### Example 2: Limit Sell Order (CLI)
```bash
$ python trading_bot/cli.py place-order BTCUSDT SELL LIMIT 0.001 --price 55000
```

### Example 3: Check Balance
```bash
$ python trading_bot/cli.py balance --asset USDT

Account Balance (USDT):
  Total Balance:    10000.0
  Available:        10000.0
  Max Withdraw:     10000.0
```

## 🧪 Testing

### Test with Sample Logs

The application logs are automatically saved to `logs/trading_bot.log`. Example log entries:

**2024-01-15 12:34:56,789 - trading_bot - INFO - client.py:145 - Attempting to place order: BUY 0.001 BTCUSDT @ MARKET**
**2024-01-15 12:34:57,123 - trading_bot - INFO - client.py:178 - Order placed successfully: Order ID 12345, Status FILLED**

### Manual Testing Checklist

- [ ] Place a MARKET BUY order
- [ ] Place a MARKET SELL order
- [ ] Place a LIMIT BUY order
- [ ] Place a LIMIT SELL order
- [ ] Check account balance
- [ ] Check order status
- [ ] Cancel a pending LIMIT order
- [ ] Verify logs in `logs/trading_bot.log`

## 🐛 Error Handling

The bot handles various error scenarios:

- **Invalid Input**: Invalid symbol format, negative quantity, missing price for LIMIT orders
- **API Errors**: Insufficient balance, invalid parameters, rate limits
- **Network Errors**: Connection timeouts, DNS failures
- **Validation Errors**: Precision mismatches, out-of-range values

All errors are logged with context and displayed to the user with helpful messages.

## 📝 Assumptions

1. **Testnet Usage**: The bot is configured for Binance Futures Testnet only
2. **USDT-M Futures**: Uses USDT-Margined futures contracts
3. **Default Asset**: USDT is the default quote currency
4. **Price/Quantity Precision**: Validates against Binance's LOT_SIZE and PRICE_FILTER rules
5. **API Rate Limits**: Respects Binance's rate limits (requests will fail with retry-after)

## 🔒 Security

- **Never share your API keys** - Store them in the `.env` file
- **Use testnet only** - This bot is not intended for live trading without thorough testing
- **Restrict API permissions** - Use API keys with minimal required permissions
- **IP whitelisting**: Consider restricting API key access to your IP address

## 🚨 Known Limitations

1. **Single Order**: No support for batch/multi-leg orders (OCO requires additional implementation)
2. **WebSocket**: No real-time data streaming (only REST API)
3. **Position Management**: No automatic position tracking or P&L calculation
4. **Stop-Limit**: Not implemented (can be added as enhancement)

## 🔄 Future Enhancements (Optional)

- [ ] Implement Stop-Limit orders
- [ ] Implement OCO (One-Cancels-the-Other) orders
- [ ] Implement TWAP (Time-Weighted Average Price) orders
- [ ] Implement Grid Trading strategy
- [ ] Add WebSocket support for real-time price updates
- [ ] Add position tracking and P&L calculation
- [ ] Add backtesting capabilities
- [ ] Add Telegram/Discord notifications
- [ ] Add trading strategy framework
- [ ] Add database for order history

## 📞 Support

If you encounter issues:

1. Check the logs in `logs/trading_bot.log`
2. Verify your API credentials are correct
3. Ensure you're connected to the internet
4. Check Binance Testnet status: https://testnet.binancefuture.com

## 📄 License

This project is provided as-is for educational and testing purposes.

## 🙏 Credits

Built with:
- [python-binance](https://github.com/sammchardy/python-binance) - Binance API wrapper
- [Typer](https://typer.tiangolo.com/) - CLI framework
- [Rich](https://rich.readthedocs.io/) - Terminal formatting
- [Colorama](https://pypi.org/project/colorama/) - Cross-platform colors

---

**Happy Trading! 📈** (On Testnet, of course!)