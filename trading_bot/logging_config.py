"""
Logging configuration for the trading bot.
"""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from rich.logging import RichHandler


def setup_logging(log_dir: str = "logs", log_level: str = "INFO") -> logging.Logger:
    """
    Configure logging with both file and console handlers.
    
    Args:
        log_dir: Directory to store log files
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Configured logger instance
    """
    # Create log directory if it doesn't exist
    Path(log_dir).mkdir(exist_ok=True)
    
    # Create logger
    logger = logging.getLogger("trading_bot")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Console handler with Rich formatting
    console_handler = RichHandler(
        rich_tracebacks=True,
        show_time=True,
        show_path=True,
        markup=True
    )
    console_formatter = logging.Formatter("%(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler with detailed formatting
    file_handler = RotatingFileHandler(
        filename=f"{log_dir}/trading_bot.log",
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding="utf-8"
    )
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    return logger


def get_logger() -> logging.Logger:
    """Get the trading bot logger instance."""
    return logging.getLogger("trading_bot")