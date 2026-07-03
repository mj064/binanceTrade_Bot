"""
Order management and business logic.
"""
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from colorama import Fore, Style, init
from bot.client import BinanceClient
from bot.validators import InputValidator
from logging_config import get_logger

# Initialize colorama for cross-platform colored output
init(autoreset=True)


@dataclass
class OrderSummary:
    """Data class representing order details."""
    symbol: str
    side: str
    order_type: str
    quantity: float
    price: Optional[float] = None
    time_in_force: str = "GTC"
    order_id: Optional[int] = None
    status: Optional[str] = None
    executed_qty: Optional[float] = None
    avg_price: Optional[float] = None
    cum_quote: Optional[float] = None
    timestamp: Optional[str] = None
    error: Optional[str] = None


class OrderManager:
    """
    Manages order operations with validation and display.
    """
    
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None):
        """
        Initialize order manager.
        
        Args:
            api_key: Binance API key
            api_secret: Binance API secret
        """
        self.logger = get_logger()
        self.client = BinanceClient(api_key, api_secret)
        self.validator = InputValidator(self.client)
    
    def validate_and_place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: str,
        price: Optional[str] = None,
        time_in_force: str = "GTC",
        reduce_only: bool = False
    ) -> OrderSummary:
        """
        Validate order parameters, place order, and return summary.
        
        Args:
            symbol: Trading pair symbol
            side: BUY or SELL
            order_type: MARKET, LIMIT, or STOP_MARKET
            quantity: Order quantity as string
            price: Order price as string (required for LIMIT)
            time_in_force: Time in force (GTC, IOC, FOK)
            reduce_only: Reduce only flag
            
        Returns:
            OrderSummary object with order details
        """
        self.logger.info(f"Starting order validation and placement for {symbol}")
        
        # Validate all inputs
        is_valid, result = self.validator.validate_all(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            time_in_force=time_in_force
        )
        
        if not is_valid:
            errors = result.get("errors", [])
            error_msg = "; ".join(errors)
            self.logger.error(f"Validation failed: {error_msg}")
            return OrderSummary(
                symbol=symbol.upper(),
                side=side.upper(),
                order_type=order_type.upper(),
                quantity=0.0,
                error=error_msg
            )
        
        # Extract validated data
        validated = result
        order_type_upper = validated["order_type"]
        
        # Place the order
        try:
            response = self.client.place_order(
                symbol=validated["symbol"],
                side=validated["side"],
                order_type=validated["order_type"],
                quantity=validated["quantity"],
                price=validated.get("price"),
                time_in_force=validated.get("time_in_force", "GTC"),
                reduce_only=reduce_only
            )
            
            # Create success summary
            summary = self._create_order_summary(validated, response)
            self._print_order_summary(summary, success=True)
            self.logger.info(f"Order completed successfully: {summary}")
            return summary
            
        except Exception as e:
            error_msg = f"Order placement failed: {str(e)}"
            self.logger.error(error_msg)
            summary = OrderSummary(
                symbol=validated["symbol"],
                side=validated["side"],
                order_type=validated["order_type"],
                quantity=validated["quantity"],
                price=validated.get("price"),
                error=error_msg
            )
            self._print_order_summary(summary, success=False)
            return summary
    
    def _create_order_summary(self, validated: Dict[str, Any], response: Dict[str, Any]) -> OrderSummary:
        """
        Create an OrderSummary from validated input and API response.
        
        Args:
            validated: Validated order parameters
            response: API response from order placement
            
        Returns:
            OrderSummary instance
        """
        return OrderSummary(
            symbol=validated["symbol"],
            side=validated["side"],
            order_type=validated["order_type"],
            quantity=validated["quantity"],
            price=validated.get("price"),
            time_in_force=validated.get("time_in_force", "GTC"),
            order_id=response["orderId"],
            status=response["status"],
            executed_qty=float(response["executedQty"]),
            avg_price=float(response["avgPrice"]) if response.get("avgPrice") else None,
            cum_quote=float(response["cumQuote"]) if response.get("cumQuote") else None,
            timestamp=response["timestamp"]
        )
    
    def _print_order_summary(self, summary: OrderSummary, success: bool = True):
        """
        Print formatted order summary to console.
        
        Args:
            summary: Order summary to print
            success: Whether the order was successful
        """
        if success:
            print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}✓ ORDER PLACED SUCCESSFULLY{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.RED}✗ ORDER FAILED{Style.RESET_ALL}")
            print(f"{Fore.RED}{'='*60}{Style.RESET_ALL}")
        
        if summary.error:
            print(f"\n{Fore.YELLOW}Error: {summary.error}{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}Order Details:{Style.RESET_ALL}")
        print(f"  Symbol:          {summary.symbol}")
        print(f"  Side:            {summary.side}")
        print(f"  Type:            {summary.order_type}")
        print(f"  Quantity:        {summary.quantity}")
        if summary.price:
            print(f"  Price:           {summary.price}")
        if summary.time_in_force:
            print(f"  Time in Force:   {summary.time_in_force}")
        
        if success:
            print(f"\n{Fore.CYAN}Execution Details:{Style.RESET_ALL}")
            print(f"  Order ID:        {summary.order_id}")
            print(f"  Status:          {summary.status}")
            print(f"  Executed Qty:    {summary.executed_qty}")
            if summary.avg_price and summary.avg_price > 0:
                print(f"  Avg Price:       {summary.avg_price}")
            if summary.cum_quote and summary.cum_quote > 0:
                print(f"  Cumulative Quote:{summary.cum_quote}")
            print(f"  Timestamp:       {summary.timestamp}")
            print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}\n")
    
    def get_account_balance(self, asset: str = "USDT") -> Optional[Dict[str, float]]:
        """
        Get and display account balance.
        
        Args:
            asset: Asset to check balance for
            
        Returns:
            Balance information dictionary or None if failed
        """
        try:
            balance = self.client.get_balance(asset)
            print(f"\n{Fore.CYAN}Account Balance ({asset}):{Style.RESET_ALL}")
            print(f"  Total Balance:    {balance['balance']}")
            print(f"  Available:        {balance['available']}")
            print(f"  Max Withdraw:     {balance['max_withdraw']}\n")
            return balance
        except Exception as e:
            self.logger.error(f"Failed to fetch balance: {e}")
            print(f"\n{Fore.RED}Error fetching balance: {e}{Style.RESET_ALL}\n")
            return None
    
    def check_order_status(self, symbol: str, order_id: int) -> Optional[Dict[str, Any]]:
        """
        Check and display order status.
        
        Args:
            symbol: Trading pair symbol
            order_id: Order ID to check
            
        Returns:
            Order status dictionary or None if failed
        """
        try:
            status = self.client.get_order_status(symbol, order_id)
            print(f"\n{Fore.CYAN}Order Status:{Style.RESET_ALL}")
            print(f"  Order ID:   {status['orderId']}")
            print(f"  Status:     {status['status']}")
            print(f"  Executed:   {status['executedQty']}")
            print(f"  Avg Price:  {status['avgPrice']}\n")
            return status
        except Exception as e:
            self.logger.error(f"Failed to fetch order status: {e}")
            print(f"\n{Fore.RED}Error fetching order status: {e}{Style.RESET_ALL}\n")
            return None
    
    def cancel_order(self, symbol: str, order_id: int):
        """
        Cancel an order.
        
        Args:
            symbol: Trading pair symbol
            order_id: Order ID to cancel
        """
        try:
            self.client.cancel_order(symbol, order_id)
            print(f"\n{Fore.GREEN}Order {order_id} cancelled successfully{Style.RESET_ALL}\n")
        except Exception as e:
            self.logger.error(f"Failed to cancel order: {e}")
            print(f"\n{Fore.RED}Error cancelling order: {e}{Style.RESET_ALL}\n")