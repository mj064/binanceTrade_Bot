#!/usr/bin/env python3
"""
Trading Bot - Main entry point for module execution.
Allows running the bot as: python -m trading_bot
"""
import sys
from pathlib import Path

# Add the trading_bot directory to path
sys.path.insert(0, str(Path(__file__).parent))

from trading_bot.cli import interactive

if __name__ == "__main__":
    interactive()