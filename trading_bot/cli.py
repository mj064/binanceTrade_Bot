#!/usr/bin/env python3
"""
Trading Bot CLI - Enhanced interactive user interface.
"""
import sys
from typing import Optional
import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

from logging_config import setup_logging, get_logger
from bot.orders import OrderManager
from bot.validators import InputValidator

# Initialize
app = typer.Typer(help="Binance Futures Testnet Trading Bot", add_completion=True)
console = Console()
logger = None


def init_bot():
    """Initialize the trading bot components."""
    global logger
    setup_logging()
    logger = get_logger()


def display_banner():
    """Display the application banner."""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║     🤖  Binance Futures Testnet Trading Bot  🤖              ║
║                                                               ║
║          Trade safely on the Binance Testnet                 ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")
    console.print("[yellow]⚠️  This is for TESTNET only. No real money involved.[/yellow]\n")


def display_menu():
    """Display the main menu options."""
    menu = """
[bold cyan]Main Menu:[/bold cyan]

  1. 📊 Check Account Balance
  2. 🛒 Place Market Order
  3. 📝 Place Limit Order
  4. 🔍 Check Order Status
  5. ❌ Cancel Order
  6. ❌ Exit
    """
    console.print(Panel(menu, border_style="blue", padding=(0, 1)))


def get_order_parameters(order_type: str) -> dict:
    """
    Get order parameters from user input with validation.
    
    Args:
        order_type: MARKET or LIMIT
        
    Returns:
        Dictionary of order parameters
    """
    params = {}
    
    # Symbol
    while True:
        symbol = Prompt.ask("Enter symbol", default="BTCUSDT").upper().strip()
        validator = InputValidator()
        is_valid, error = validator.validate_symbol(symbol)
        if is_valid:
            params["symbol"] = symbol
            break
        console.print(f"[red]✗ Invalid symbol: {error}[/red]")
    
    # Side
    while True:
        side = Prompt.ask("Enter side", choices=["BUY", "SELL"], default="BUY").upper().strip()
        validator = InputValidator()
        is_valid, error = validator.validate_side(side)
        if is_valid:
            params["side"] = side
            break
        console.print(f"[red]✗ Invalid side: {error}[/red]")
    
    # Quantity
    while True:
        quantity = Prompt.ask("Enter quantity")
        validator = InputValidator()
        is_valid, error, qty = validator.validate_quantity(quantity)
        if is_valid:
            params["quantity"] = str(qty)
            params["quantity_float"] = qty
            break
        console.print(f"[red]✗ Invalid quantity: {error}[/red]")
    
    # Price (for LIMIT orders)
    if order_type == "LIMIT":
        while True:
            price = Prompt.ask("Enter price")
            validator = InputValidator()
            is_valid, error, p = validator.validate_price(price)
            if is_valid:
                params["price"] = str(p)
                params["price_float"] = p
                break
            console.print(f"[red]✗ Invalid price: {error}[/red]")
        
        # Time in force
        params["time_in_force"] = Prompt.ask(
            "Enter time in force",
            choices=["GTC", "IOC", "FOK"],
            default="GTC"
        ).upper().strip()
    
    return params


@app.command()
def interactive():
    """Run the enhanced interactive CLI mode."""
    init_bot()
    display_banner()
    
    manager = OrderManager()
    
    while True:
        display_menu()
        choice = Prompt.ask("\n[bold cyan]Select option[/bold cyan]", choices=["1", "2", "3", "4", "5", "6"], default="6")
        
        if choice == "1":
            console.print("\n[bold yellow]Fetching account balance...[/bold yellow]")
            asset = Prompt.ask("Enter asset", default="USDT").upper().strip()
            manager.get_account_balance(asset)
            
        elif choice == "2":
            console.print("\n[bold yellow]Placing MARKET Order[/bold yellow]")
            params = get_order_parameters("MARKET")
            
            console.print(f"\n[yellow]Order Summary:[/yellow]")
            console.print(f"  {params['side']} {params['quantity_float']} {params['symbol']} @ MARKET")
            
            if Confirm.ask("\n[yellow]Confirm order?[/yellow]", default=True):
                manager.validate_and_place_order(
                    symbol=params["symbol"],
                    side=params["side"],
                    order_type="MARKET",
                    quantity=params["quantity"]
                )
            else:
                console.print("[yellow]Order cancelled by user[/yellow]")
            
        elif choice == "3":
            console.print("\n[bold yellow]Placing LIMIT Order[/bold yellow]")
            params = get_order_parameters("LIMIT")
            
            # Display summary
            console.print(f"\n[yellow]Order Summary:[/yellow]")
            console.print(f"  {params['side']} {params['quantity_float']} {params['symbol']} @ {params['price_float']}")
            console.print(f"  Time in Force: {params['time_in_force']}")
            
            if Confirm.ask("\n[yellow]Confirm order?[/yellow]", default=True):
                manager.validate_and_place_order(
                    symbol=params["symbol"],
                    side=params["side"],
                    order_type="LIMIT",
                    quantity=params["quantity"],
                    price=params["price"],
                    time_in_force=params["time_in_force"]
                )
            else:
                console.print("[yellow]Order cancelled by user[/yellow]")
            
        elif choice == "4":
            console.print("\n[bold yellow]Check Order Status[/bold yellow]")
            symbol = Prompt.ask("Enter symbol", default="BTCUSDT").upper().strip()
            order_id = int(Prompt.ask("Enter order ID"))
            manager.check_order_status(symbol, order_id)
            
        elif choice == "5":
            console.print("\n[bold yellow]Cancel Order[/bold yellow]")
            symbol = Prompt.ask("Enter symbol", default="BTCUSDT").upper().strip()
            order_id = int(Prompt.ask("Enter order ID"))
            
            if Confirm.ask(f"\n[yellow]Cancel order {order_id} for {symbol}?[/yellow]", default=False):
                manager.cancel_order(symbol, order_id)
            else:
                console.print("[yellow]Cancellation aborted[/yellow]")
            
        elif choice == "6":
            console.print("\n[green]Thank you for using the Trading Bot! 👋[/green]\n")
            sys.exit(0)
        
        # Pause before showing menu again
        Prompt.ask("\n[dim]Press Enter to continue...[/dim]", default="")


@app.command()
def place_order(
    symbol: str = typer.Argument(..., help="Trading pair symbol"),
    side: str = typer.Argument(..., help="Order side: BUY or SELL"),
    order_type: str = typer.Argument(..., help="Order type: MARKET, LIMIT, or STOP_MARKET"),
    quantity: str = typer.Argument(..., help="Order quantity"),
    price: Optional[str] = typer.Option(None, "--price", "-p", help="Order price"),
    time_in_force: str = typer.Option("GTC", "--tif", help="Time in force: GTC, IOC, or FOK"),
    reduce_only: bool = typer.Option(False, "--reduce-only", help="Reduce only flag"),
    balance: bool = typer.Option(False, "--balance", help="Show balance after order"),
):
    """
    Place an order on Binance Futures Testnet.
    
    Example usage:
        python cli.py place-order BTCUSDT BUY MARKET 0.001
        python cli.py place-order BTCUSDT SELL LIMIT 0.001 --price 50000
    """
    init_bot()
    
    # Validate order type
    validator = InputValidator()
    is_valid, error = validator.validate_order_type(order_type)
    if not is_valid:
        console.print(f"[red]✗ Invalid order type: {error}[/red]")
        raise typer.Exit(1)
    
    # Check if price is provided for LIMIT orders
    order_type_upper = order_type.upper()
    if order_type_upper == "LIMIT" and not price:
        console.print("[red]✗ Price is required for LIMIT orders. Use --price option.[/red]")
        raise typer.Exit(1)
    
    manager = OrderManager()
    summary = manager.validate_and_place_order(
        symbol=symbol,
        side=side,
        order_type=order_type_upper,
        quantity=quantity,
        price=price,
        time_in_force=time_in_force,
        reduce_only=reduce_only
    )
    
    if balance and summary.order_id:
        Prompt.ask("\n[dim]Press Enter to show balance...[/dim]", default="")
        manager.get_account_balance()
    
    if summary.error:
        raise typer.Exit(1)


@app.command()
def balance(
    asset: str = typer.Option("USDT", "--asset", "-a", help="Asset to check balance for")
):
    """
    Check your account balance.
    
    Example:
        python cli.py balance
        python cli.py balance --asset BTC
    """
    init_bot()
    manager = OrderManager()
    manager.get_account_balance(asset)


@app.command()
def status(
    symbol: str = typer.Argument(..., help="Trading pair symbol"),
    order_id: int = typer.Argument(..., help="Order ID to check")
):
    """
    Check the status of an order.
    
    Example:
        python cli.py status BTCUSDT 12345
    """
    init_bot()
    manager = OrderManager()
    manager.check_order_status(symbol.upper(), order_id)


@app.command()
def cancel(
    symbol: str = typer.Argument(..., help="Trading pair symbol"),
    order_id: int = typer.Argument(..., help="Order ID to cancel")
):
    """
    Cancel an existing order.
    
    Example:
        python cli.py cancel BTCUSDT 12345
    """
    init_bot()
    manager = OrderManager()
    manager.cancel_order(symbol.upper(), order_id)


@app.command()
def menu():
    """Launch the interactive menu mode."""
    interactive()


if __name__ == "__main__":
    # If no arguments provided, run interactive mode by default
    if len(sys.argv) == 1:
        try:
            interactive()
        except Exception:
            app()
    else:
        app()
