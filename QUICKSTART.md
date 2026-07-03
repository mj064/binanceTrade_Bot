# 🚀 Quick Start Guide

## 1. Setup (5 minutes)

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure API Credentials
Edit `.env` file with your Binance Futures Testnet credentials:
```env
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
```

**Get testnet credentials**: https://testnet.binancefuture.com/

## 2. Run the Bot

### Interactive Mode (Recommended)
```bash
python trading_bot/cli.py
```
or
```bash
cd trading_bot
python cli.py
```

### Command Line Mode
```bash
# Market order
python trading_bot/cli.py place-order BTCUSDT BUY MARKET 0.001

# Limit order
python trading_bot/cli.py place-order BTCUSDT SELL LIMIT 0.001 --price 50000

# Check balance
python trading_bot/cli.py balance

# Check order status
python trading_bot/cli.py status BTCUSDT 12345

# Cancel order
python trading_bot/cli.py cancel BTCUSDT 12345
```

## 3. Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `place-order` | Place a new order | `python cli.py place-order BTCUSDT BUY MARKET 0.001` |
| `balance` | Check account balance | `python cli.py balance --asset USDT` |
| `status` | Check order status | `python cli.py status BTCUSDT 12345` |
| `cancel` | Cancel an order | `python cli.py cancel BTCUSDT 12345` |
| `menu` | Open interactive menu | `python cli.py menu` |
| `interactive` | Open interactive menu | `python cli.py interactive` |

## 4. Order Types Supported

- **MARKET** - Execute immediately at market price
- **LIMIT** - Execute at specified price or better
- **STOP_MARKET** - Trigger market order when price hits stop price

## 5. Order Sides

- **BUY** - Buy/Long position
- **SELL** - Sell/Short position

## 6. Project Structure

```
trading_bot/
├── trading_bot/           # Main package
│   ├── bot/               # Core business logic
│   │   ├── __init__.py
│   │   ├── client.py      # Binance API wrapper
│   │   ├── orders.py      # Order management
│   │   └── validators.py  # Input validation
│   ├── logging_config.py  # Logging setup
│   ├── __main__.py        # Module entry point
│   └── cli.py             # CLI interface
├── logs/                  # Log files
│   ├── sample_market_order.log
│   └── sample_limit_order.log
├── requirements.txt       # Python dependencies
├── README.md             # Full documentation
└── .env                  # API credentials
```

## 7. Features Implemented

✅ Market and Limit orders on Binance Futures Testnet
✅ BUY and SELL support
✅ Enhanced CLI with interactive menu (Typer + Rich)
✅ Input validation with detailed error messages
✅ Comprehensive logging to file and console
✅ Exception handling for API errors, network failures, invalid input
✅ Clear order summaries and execution details
✅ Balance checking
✅ Order status checking
✅ Order cancellation
✅ STOP_MARKET order support
✅ Colorful terminal output

## 8. Testing

The project includes sample log files demonstrating:
- MARKET order execution (`logs/sample_market_order.log`)
- LIMIT order execution (`logs/sample_limit_order.log`)

## 9. Troubleshooting

**Module not found errors?**
```bash
cd trading_bot
python cli.py --help
```

**API connection issues?**
- Verify your testnet credentials in `.env`
- Check internet connection
- Visit https://testnet.binancefuture.com/ to confirm service status

**Import errors?**
```bash
pip install --upgrade python-binance typer rich colorama python-dotenv
```

## 10. Important Notes

⚠️ **Testnet Only**: This bot is configured for Binance Futures Testnet. No real money is involved.

📝 **Logs**: All API requests, responses, and errors are logged to `logs/trading_bot.log`

🔒 **Security**: Never share your `.env` file or commit it to version control

---

**Ready to trade?** Run `python trading_bot/cli.py` and select option 2 or 3!