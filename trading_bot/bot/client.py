"""
Binance Futures Testnet client wrapper.
"""
import os
import time
from typing import Dict, Any, Optional
from datetime import datetime
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from dotenv import load_dotenv
from logging_config import get_logger

load_dotenv()


class BinanceClient:
    """
    Wrapper for Binance Futures Testnet API client.
    """
    
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None):
        """
        Initialize Binance client with API credentials.
        
        Args:
            api_key: Binance API key (defaults to env var BINANCE_API_KEY)
            api_secret: Binance API secret (defaults to env var BINANCE_API_SECRET)
        """
        self.logger = get_logger()
        self.logger.info("Initializing Binance client...")
        
        self.api_key = api_key or os.getenv("BINANCE_API_KEY", "")
        self.api_secret = api_secret or os.getenv("BINANCE_API_SECRET", "")
        self.base_url = "https://testnet.binancefuture.com"
        
        if not self.api_key or not self.api_secret:
            self.logger.warning("API credentials not provided. Set BINANCE_API_KEY and BINANCE_API_SECRET env vars.")
        
        try:
            self.client = Client(api_key=self.api_key, api_secret=self.api_secret)
            self.client.API_URL = f"{self.base_url}/api"
            self.client.FUTURES_URL = f"{self.base_url}/fapi"
            
            # Test connection
            self._test_connection()
            self.logger.info("Binance client initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Binance client: {e}")
            raise
    
    def _test_connection(self):
        """Test connection to Binance API."""
        try:
            server_time = self.client.futures_time()
            self.client.timestamp_offset = server_time['serverTime'] - int(time.time() * 1000)
            self.logger.info(f"Connected to testnet. Time offset: {self.client.timestamp_offset}ms")
        except BinanceAPIException as e:
            self.logger.error(f"API connection test failed: {e}")
            raise
    
    def get_balance(self, asset: str = "USDT") -> Dict[str, Any]:
        """
        Get futures account balance.
        
        Args:
            asset: Asset to check balance for (default: USDT)
            
        Returns:
            Dictionary containing balance information
        """
        self.logger.info(f"Fetching balance for {asset}...")
        try:
            balance = self.client.futures_account_balance()
            asset_balance = next((item for item in balance if item["asset"] == asset), None)
            
            if asset_balance:
                result = {
                    "asset": asset_balance["asset"],
                    "balance": float(asset_balance["balance"]),
                    "available": float(asset_balance["availableBalance"]),
                    "max_withdraw": float(asset_balance["maxWithdrawAmount"])
                }
                self.logger.info(f"Balance retrieved: {result}")
                return result
            else:
                self.logger.warning(f"Asset {asset} not found in balance")
                return {"asset": asset, "balance": 0.0, "available": 0.0}
                
        except BinanceAPIException as e:
            self.logger.error(f"API error fetching balance: {e.status_code} - {e.message}")
            raise
        except Exception as e:
            self.logger.error(f"Error fetching balance: {e}")
            raise
    
    def get_symbol_info(self, symbol: str) -> Dict[str, Any]:
        """
        Get symbol information including lot size, tick size, etc.
        
        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT)
            
        Returns:
            Dictionary containing symbol information
        """
        self.logger.info(f"Fetching symbol info for {symbol}...")
        try:
            info = self.client.futures_exchange_info()
            symbol_info = next((item for item in info["symbols"] if item["symbol"] == symbol), None)
            
            if not symbol_info:
                raise ValueError(f"Symbol {symbol} not found")
            
            self.logger.info(f"Symbol info retrieved for {symbol}")
            return {
                "symbol": symbol_info["symbol"],
                "status": symbol_info["status"],
                "baseAsset": symbol_info["baseAsset"],
                "quoteAsset": symbol_info["quoteAsset"],
                "filters": {f["filterType"]: f for f in symbol_info.get("filters", [])}
            }
            
        except BinanceAPIException as e:
            self.logger.error(f"API error fetching symbol info: {e.status_code} - {e.message}")
            raise
        except Exception as e:
            self.logger.error(f"Error fetching symbol info: {e}")
            raise
    
    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
        time_in_force: str = "GTC",
        reduce_only: bool = False
    ) -> Dict[str, Any]:
        """
        Place an order on Binance Futures Testnet.
        
        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT)
            side: BUY or SELL
            order_type: MARKET, LIMIT, STOP_MARKET, etc.
            quantity: Order quantity
            price: Order price (required for LIMIT orders)
            time_in_force: Time in force (GTC, IOC, FOK)
            reduce_only: Whether to close positions only
            
        Returns:
            Dictionary containing order response details
        """
        self.logger.info(f"Attempting to place order: {side} {quantity} {symbol} @ {order_type}")
        
        try:
            # Validate inputs
            if side not in ("BUY", "SELL"):
                raise ValueError("Side must be BUY or SELL")
            
            if order_type not in ("MARKET", "LIMIT", "STOP_MARKET"):
                raise ValueError(f"Unsupported order type: {order_type}")
            
            if order_type == "LIMIT" and price is None:
                raise ValueError("Price is required for LIMIT orders")
            
            # Prepare order parameters
            order_params = {
                "symbol": symbol,
                "side": side,
                "type": order_type,
                "quantity": quantity
            }
            
            if order_type == "LIMIT":
                order_params["price"] = price
                order_params["timeInForce"] = time_in_force
            
            if reduce_only:
                order_params["reduceOnly"] = reduce_only
            
            # Log the request
            self.logger.debug(f"Order parameters: {order_params}")
            
            # Place order
            response = self.client.futures_create_order(**order_params)
            
            # Format response
            result = {
                "orderId": response["orderId"],
                "symbol": response["symbol"],
                "status": response["status"],
                "clientOrderId": response["clientOrderId"],
                "side": response["side"],
                "type": response["type"],
                "quantity": response["origQty"],
                "executedQty": response["executedQty"],
                "avgPrice": response.get("avgPrice", 0.0),
                "cumQuote": response.get("cumQuote", 0.0),
                "timestamp": datetime.fromtimestamp(response["updateTime"] / 1000).isoformat()
            }
            
            self.logger.info(f"Order placed successfully: Order ID {result['orderId']}, Status {result['status']}")
            self.logger.debug(f"Full response: {response}")
            
            return result
            
        except BinanceAPIException as e:
            self.logger.error(f"Binance API error: {e.status_code} - {e.message}")
            raise
        except BinanceRequestException as e:
            self.logger.error(f"Binance request error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error placing order: {e}")
            raise
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """
        Cancel an existing order.
        
        Args:
            symbol: Trading pair symbol
            order_id: Order ID to cancel
            
        Returns:
            Cancellation response details
        """
        self.logger.info(f"Cancelling order {order_id} for {symbol}...")
        try:
            response = self.client.futures_cancel_order(symbol=symbol, orderId=order_id)
            self.logger.info(f"Order cancelled: {order_id}")
            return response
        except Exception as e:
            self.logger.error(f"Error cancelling order: {e}")
            raise
    
    def get_order_status(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """
        Get order status.
        
        Args:
            symbol: Trading pair symbol
            order_id: Order ID to check
            
        Returns:
            Order status details
        """
        self.logger.info(f"Fetching status for order {order_id}...")
        try:
            response = self.client.futures_get_order(symbol=symbol, orderId=order_id)
            return {
                "orderId": response["orderId"],
                "status": response["status"],
                "executedQty": response["executedQty"],
                "avgPrice": response.get("avgPrice", 0.0)
            }
        except Exception as e:
            self.logger.error(f"Error fetching order status: {e}")
            raise