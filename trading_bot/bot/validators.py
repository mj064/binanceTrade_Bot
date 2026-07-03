"""
Input validation module for trading bot.
"""
import re
from typing import Tuple, Optional
from binance.client import Client
from bot.client import BinanceClient
from logging_config import get_logger


class InputValidator:
    """
    Validates user inputs for trading operations.
    """
    
    def __init__(self, binance_client: Optional[BinanceClient] = None):
        """
        Initialize validator.
        
        Args:
            binance_client: Optional BinanceClient instance for symbol validation
        """
        self.logger = get_logger()
        self.client = binance_client
        self._supported_symbols = None
    
    def validate_symbol(self, symbol: str) -> Tuple[bool, str]:
        """
        Validate trading symbol format and existence.
        
        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT)
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not symbol:
            return False, "Symbol is required"
        
        symbol = symbol.upper().strip()
        
        # Basic format check (should be like BTCUSDT, ETHUSDT, etc.)
        if not re.match(r'^[A-Z]{2,10}USDT$', symbol):
            return False, "Invalid symbol format. Expected format: BTCUSDT, ETHUSDT, etc."
        
        # NOTE: In production, you'd validate against actual exchange info
        # self._validate_symbol_exists(symbol)
        
        return True, ""
    
    def validate_side(self, side: str) -> Tuple[bool, str]:
        """
        Validate order side.
        
        Args:
            side: BUY or SELL
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not side:
            return False, "Side is required"
        
        side = side.upper().strip()
        
        if side not in ("BUY", "SELL"):
            return False, "Side must be BUY or SELL"
        
        return True, ""
    
    def validate_order_type(self, order_type: str) -> Tuple[bool, str]:
        """
        Validate order type.
        
        Args:
            order_type: MARKET, LIMIT, or STOP_MARKET
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not order_type:
            return False, "Order type is required"
        
        order_type = order_type.upper().strip()
        
        valid_types = ("MARKET", "LIMIT", "STOP_MARKET", "STOP")
        if order_type not in valid_types:
            return False, f"Invalid order type. Must be one of: {', '.join(valid_types)}"
        
        return True, ""
    
    def validate_quantity(self, quantity: str, symbol_info: Optional[dict] = None) -> Tuple[bool, str, float]:
        """
        Validate order quantity.
        
        Args:
            quantity: Order quantity as string
            symbol_info: Optional symbol info for precision validation
            
        Returns:
            Tuple of (is_valid, error_message, parsed_quantity)
        """
        if not quantity:
            return False, "Quantity is required", 0.0
        
        try:
            qty = float(quantity)
        except ValueError:
            return False, "Quantity must be a valid number", 0.0
        
        if qty <= 0:
            return False, "Quantity must be greater than 0", 0.0
        
        # Validate precision against symbol info if available
        if symbol_info and "filters" in symbol_info:
            lot_size_filter = symbol_info["filters"].get("LOT_SIZE")
            if lot_size_filter:
                min_qty = float(lot_size_filter.get("minQty", 0))
                max_qty = float(lot_size_filter.get("maxQty", float('inf')))
                step_size = float(lot_size_filter.get("stepSize", 0))
                
                if qty < min_qty:
                    return False, f"Quantity must be >= {min_qty}", 0.0
                
                if qty > max_qty:
                    return False, f"Quantity must be <= {max_qty}", 0.0
                
                if step_size > 0:
                    # Validate step size precision
                    precision = len(str(step_size).rstrip('0').split('.')[-1])
                    rounded_qty = round(qty, precision)
                    if qty != rounded_qty:
                        return False, f"Quantity precision error. Must be multiple of {step_size}", qty
        
        return True, "", qty
    
    def validate_price(self, price: str, symbol_info: Optional[dict] = None) -> Tuple[bool, str, float]:
        """
        Validate order price.
        
        Args:
            price: Order price as string
            symbol_info: Optional symbol info for precision validation
            
        Returns:
            Tuple of (is_valid, error_message, parsed_price)
        """
        if not price:
            return False, "Price is required for LIMIT orders", 0.0
        
        try:
            p = float(price)
        except ValueError:
            return False, "Price must be a valid number", 0.0
        
        if p <= 0:
            return False, "Price must be greater than 0", 0.0
        
        # Validate precision against symbol info if available
        if symbol_info and "filters" in symbol_info:
            price_filter = symbol_info["filters"].get("PRICE_FILTER")
            if price_filter:
                tick_size = float(price_filter.get("tickSize", 0))
                min_price = float(price_filter.get("minPrice", 0))
                max_price = float(price_filter.get("maxPrice", float('inf')))
                
                if p < min_price:
                    return False, f"Price must be >= {min_price}", 0.0
                
                if p > max_price:
                    return False, f"Price must be <= {max_price}", 0.0
                
                if tick_size > 0:
                    precision = len(str(tick_size).rstrip('0').split('.')[-1])
                    rounded_price = round(p, precision)
                    if p != rounded_price:
                        return False, f"Price precision error. Must be multiple of {tick_size}", p
        
        return True, "", p
    
    def validate_time_in_force(self, tif: str) -> Tuple[bool, str]:
        """
        Validate time in force parameter.
        
        Args:
            tif: Time in force (GTC, IOC, FOK)
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not tif:
            return False, "Time in force is required"
        
        tif = tif.upper().strip()
        valid_tifs = ("GTC", "IOC", "FOK")
        
        if tif not in valid_tifs:
            return False, f"Invalid time in force. Must be one of: {', '.join(valid_tifs)}"
        
        return True, ""
    
    def validate_all(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: str,
        price: Optional[str] = None,
        time_in_force: str = "GTC"
    ) -> Tuple[bool, dict]:
        """
        Validate all order parameters.
        
        Args:
            symbol: Trading pair symbol
            side: BUY or SELL
            order_type: MARKET, LIMIT, etc.
            quantity: Order quantity
            price: Order price (optional)
            time_in_force: Time in force for LIMIT orders
            
        Returns:
            Tuple of (is_valid, validated_data_or_errors)
        """
        errors = []
        validated_data = {}
        
        # Validate symbol
        is_valid, error = self.validate_symbol(symbol)
        if not is_valid:
            errors.append(f"Symbol: {error}")
        else:
            validated_data["symbol"] = symbol.upper().strip()
        
        # Validate side
        is_valid, error = self.validate_side(side)
        if not is_valid:
            errors.append(f"Side: {error}")
        else:
            validated_data["side"] = side.upper().strip()
        
        # Validate order type
        is_valid, error = self.validate_order_type(order_type)
        if not is_valid:
            errors.append(f"Order Type: {error}")
        else:
            validated_data["order_type"] = order_type.upper().strip()
        
        # Get symbol info for quantity/price validation
        symbol_info = None
        if self.client and validated_data.get("symbol"):
            try:
                symbol_info = self.client.get_symbol_info(validated_data["symbol"])
            except Exception as e:
                self.logger.warning(f"Could not fetch symbol info: {e}")
        
        # Validate quantity
        is_valid, error, qty = self.validate_quantity(quantity, symbol_info)
        if not is_valid:
            errors.append(f"Quantity: {error}")
        else:
            validated_data["quantity"] = qty
        
        # Validate price if provided or required
        if order_type.upper() == "LIMIT" or price:
            is_valid, error, p = self.validate_price(price, symbol_info)
            if not is_valid:
                errors.append(f"Price: {error}")
            else:
                validated_data["price"] = p
        
        # Validate time in force for LIMIT orders
        if order_type.upper() == "LIMIT":
            is_valid, error = self.validate_time_in_force(time_in_force)
            if not is_valid:
                errors.append(f"Time In Force: {error}")
            else:
                validated_data["time_in_force"] = time_in_force.upper().strip()
        
        if errors:
            return False, {"errors": errors}
        
        return True, validated_data