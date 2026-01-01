"""
Binance Futures Trading Bot - Main CLI Interface
Unified command-line interface for all order types:
- Market Orders
- Limit Orders
- TWAP Orders
"""

import sys
import argparse
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from market_orders import validate_inputs as validate_market, place_market_order
from limit_orders import validate_inputs as validate_limit, place_limit_order
from logger import logger


def validate_twap_inputs(symbol: str, total_qty: float, price: float, chunks: int, interval: int):
    """Validate TWAP inputs"""
    if not symbol.isalnum():
        raise ValueError("Invalid symbol format")
    if total_qty <= 0:
        raise ValueError("Total quantity must be greater than 0")
    if price <= 0:
        raise ValueError("Price must be greater than 0")
    if chunks <= 0:
        raise ValueError("Number of chunks must be greater than 0")
    if interval <= 0:
        raise ValueError("Interval must be greater than 0")


def execute_market_order(args):
    """Execute market order"""
    try:
        validate_market(args.symbol, args.side, args.quantity)
        result = place_market_order(args.symbol, args.side, args.quantity)
        
        print("\n" + "="*70)
        print("MARKET ORDER EXECUTED")
        print("="*70)
        print(f"Symbol: {args.symbol}")
        print(f"Side: {args.side}")
        print(f"Quantity: {args.quantity}")
        print(f"Order ID: {result.get('orderId')}")
        print(f"Status: {result.get('status')}")
        print("="*70 + "\n")
        
        return 0
    except Exception as e:
        logger.error(f"Market order failed: {str(e)}")
        print(f"❌ Error: {e}")
        return 1


def execute_limit_order(args):
    """Execute limit order"""
    try:
        validate_limit(args.symbol, args.side, args.quantity, args.price)
        result = place_limit_order(args.symbol, args.side, args.quantity, args.price)
        
        order_id = result.get('orderId') or result.get('id') or 'N/A'
        
        print("\n" + "="*70)
        print("LIMIT ORDER PLACED")
        print("="*70)
        print(f"Symbol: {args.symbol}")
        print(f"Side: {args.side}")
        print(f"Quantity: {args.quantity}")
        print(f"Price: ${args.price}")
        print(f"Order ID: {order_id}")
        print(f"Status: {result.get('status', 'PENDING')}")
        print("="*70 + "\n")
        
        return 0
    except Exception as e:
        logger.error(f"Limit order failed: {str(e)}")
        print(f"❌ Error: {e}")
        return 1


def execute_twap_order(args):
    """Execute TWAP order"""
    try:
        validate_twap_inputs(args.symbol, args.quantity, args.price, args.chunks, args.interval)
        
        # Import TWAP module
        from advanced.twap import place_twap_order, print_twap_result
        
        result = place_twap_order(
            args.symbol,
            args.side,
            args.quantity,
            args.price,
            args.chunks,
            args.interval,
            dry_run=args.dry_run
        )
        
        print_twap_result(result)
        return 0
    except Exception as e:
        logger.error(f"TWAP order failed: {str(e)}")
        print(f"❌ Error: {e}")
        return 1


def create_parser():
    """Create argument parser for CLI"""
    parser = argparse.ArgumentParser(
        description="🤖 Binance Futures Trading Bot - Trade with multiple order types",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Market Order:
    python bot.py market -s BTCUSDT -sd BUY -q 0.01
  
  Limit Order:
    python bot.py limit -s BTCUSDT -sd BUY -q 0.01 -p 40000
  
  TWAP Order (with dry-run):
    python bot.py twap -s BTCUSDT -sd BUY -q 1.0 -p 40000 -c 5 -i 60 --dry-run
  
  TWAP Order (live):
    python bot.py twap -s BTCUSDT -sd BUY -q 1.0 -p 40000 -c 5 -i 60
        """
    )

    subparsers = parser.add_subparsers(dest="order_type", help="Order type to execute")

    # Market Order Subparser
    market_parser = subparsers.add_parser("market", help="Place a market order")
    market_parser.add_argument("-s", "--symbol", required=True, help="Trading pair (e.g., BTCUSDT)")
    market_parser.add_argument("-sd", "--side", required=True, choices=["BUY", "SELL"], help="Order side")
    market_parser.add_argument("-q", "--quantity", type=float, required=True, help="Order quantity")

    # Limit Order Subparser
    limit_parser = subparsers.add_parser("limit", help="Place a limit order")
    limit_parser.add_argument("-s", "--symbol", required=True, help="Trading pair (e.g., BTCUSDT)")
    limit_parser.add_argument("-sd", "--side", required=True, choices=["BUY", "SELL"], help="Order side")
    limit_parser.add_argument("-q", "--quantity", type=float, required=True, help="Order quantity")
    limit_parser.add_argument("-p", "--price", type=float, required=True, help="Limit price")

    # TWAP Order Subparser
    twap_parser = subparsers.add_parser("twap", help="Place a TWAP order (split into chunks)")
    twap_parser.add_argument("-s", "--symbol", required=True, help="Trading pair (e.g., BTCUSDT)")
    twap_parser.add_argument("-sd", "--side", required=True, choices=["BUY", "SELL"], help="Order side")
    twap_parser.add_argument("-q", "--quantity", type=float, required=True, help="Total quantity to trade")
    twap_parser.add_argument("-p", "--price", type=float, required=True, help="Limit price for all chunks")
    twap_parser.add_argument("-c", "--chunks", type=int, required=True, help="Number of chunks to split into")
    twap_parser.add_argument("-i", "--interval", type=int, required=True, help="Interval between chunks (seconds)")
    twap_parser.add_argument("--dry-run", action="store_true", help="Preview execution plan without placing orders")

    return parser


def main():
    """Main CLI entry point"""
    parser = create_parser()
    
    # Print help if no arguments
    if len(sys.argv) == 1:
        parser.print_help()
        return 1

    args = parser.parse_args()

    logger.info(f"Bot started | Order Type: {args.order_type}")

    try:
        if args.order_type == "market":
            return execute_market_order(args)
        elif args.order_type == "limit":
            return execute_limit_order(args)
        elif args.order_type == "twap":
            return execute_twap_order(args)
        else:
            print("❌ Unknown order type. Use 'python bot.py -h' for help.")
            return 1

    except KeyboardInterrupt:
        logger.warning("Bot interrupted by user")
        print("\n⚠️  Bot interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        print(f"❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
