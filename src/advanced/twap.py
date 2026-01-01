"""
TWAP (Time-Weighted Average Price) Order Implementation
Splits a large order into smaller chunks and executes them at regular intervals.
This helps minimize market impact and achieve better average prices.
"""

import sys
import time
from config import client
from logger import logger


def validate_twap_inputs(
    symbol: str,
    side: str,
    total_quantity: float,
    price: float,
    num_chunks: int,
    interval_seconds: int
):
    """Validate TWAP order inputs"""
    if not symbol.isalnum():
        raise ValueError("Invalid symbol format")

    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be BUY or SELL")

    if total_quantity <= 0:
        raise ValueError("Total quantity must be greater than 0")

    if price <= 0:
        raise ValueError("Price must be greater than 0")

    if num_chunks <= 0:
        raise ValueError("Number of chunks must be greater than 0")

    if interval_seconds <= 0:
        raise ValueError("Interval must be greater than 0 seconds")


def calculate_chunk_size(total_quantity: float, num_chunks: int) -> tuple:
    """
    Calculate chunk sizes for TWAP execution
    
    Args:
        total_quantity: Total order quantity
        num_chunks: Number of chunks to split into
    
    Returns:
        Tuple of (chunk_quantity, remainder_quantity)
    """
    chunk_quantity = total_quantity / num_chunks
    # For float division, remainder is minimal - just use equal chunks
    return chunk_quantity, 0.0


def place_twap_order(
    symbol: str,
    side: str,
    total_quantity: float,
    price: float,
    num_chunks: int,
    interval_seconds: int,
    dry_run: bool = False
):
    """
    Execute TWAP order by placing multiple smaller orders at intervals
    
    Args:
        symbol: Trading pair (e.g., BTCUSDT)
        side: BUY or SELL
        total_quantity: Total quantity to trade
        price: Limit price for all orders
        num_chunks: Number of chunks to split into
        interval_seconds: Seconds between each order
        dry_run: If True, show execution plan without placing orders
    
    Returns:
        Dictionary with execution details and order IDs
    """
    chunk_size, remainder = calculate_chunk_size(total_quantity, num_chunks)

    logger.info(
        f"Starting TWAP execution | {symbol} | {side} | "
        f"total_qty={total_quantity} | chunks={num_chunks} | "
        f"interval={interval_seconds}s | chunk_size={chunk_size:.8f}"
    )

    if dry_run:
        print("\n" + "="*70)
        print("TWAP EXECUTION PLAN (DRY RUN - NO ORDERS PLACED)")
        print("="*70)
        print(f"Symbol: {symbol}")
        print(f"Side: {side}")
        print(f"Total Quantity: {total_quantity}")
        print(f"Price: {price}")
        print(f"Number of Chunks: {num_chunks}")
        print(f"Interval: {interval_seconds} seconds")
        print(f"Chunk Size: {chunk_size:.8f}")
        print(f"Remainder: {remainder:.8f}")
        print("\nExecution Schedule:")
        print("-" * 70)

        total_time = (num_chunks - 1) * interval_seconds
        for i in range(1, num_chunks + 1):
            time_offset = (i - 1) * interval_seconds
            qty = chunk_size + (remainder if i == num_chunks else 0)
            print(
                f"Order {i}: {qty:.8f} {symbol} at ${price} "
                f"(+{time_offset}s from start)"
            )

        print("-" * 70)
        print(f"Total Execution Time: {total_time} seconds (~{total_time/60:.1f} minutes)")
        print("="*70 + "\n")
        return {"dry_run": True, "planned_orders": num_chunks}

    # Execute TWAP orders
    order_ids = []
    executed_quantity = 0

    try:
        for i in range(1, num_chunks + 1):
            # Calculate quantity for this chunk (add remainder to last chunk)
            chunk_qty = chunk_size + (remainder if i == num_chunks else 0)

            logger.info(
                f"Executing chunk {i}/{num_chunks} | qty={chunk_qty:.8f} | "
                f"price={price}"
            )

            # Place limit order
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                quantity=round(chunk_qty, 8),  # Round to 8 decimals
                price=price,
                timeInForce="GTC"
            )

            order_id = order.get("orderId")
            order_ids.append(order_id)
            executed_quantity += chunk_qty

            logger.info(
                f"Chunk {i} order placed | Order ID: {order_id} | "
                f"Total executed so far: {executed_quantity:.8f}"
            )

            print(f"✓ Order {i}/{num_chunks} placed (Order ID: {order_id})")

            # Wait for interval before next order (except for last order)
            if i < num_chunks:
                logger.info(f"Waiting {interval_seconds}s before next chunk...")
                time.sleep(interval_seconds)

        result = {
            "symbol": symbol,
            "side": side,
            "total_quantity": total_quantity,
            "executed_quantity": executed_quantity,
            "price": price,
            "num_chunks": num_chunks,
            "interval_seconds": interval_seconds,
            "order_ids": order_ids,
            "status": "completed"
        }

        logger.info(
            f"TWAP execution completed | Orders: {order_ids} | "
            f"Total Quantity: {executed_quantity:.8f}"
        )
        return result

    except Exception as e:
        logger.error(f"TWAP execution failed: {str(e)}")
        raise


def print_twap_result(result: dict):
    """Print formatted TWAP execution results"""
    if result.get("dry_run"):
        return  # Already printed in place_twap_order

    print("\n" + "="*70)
    print("TWAP ORDER EXECUTION COMPLETED")
    print("="*70)
    print(f"Symbol: {result['symbol']}")
    print(f"Side: {result['side']}")
    print(f"Total Quantity: {result['total_quantity']:.8f}")
    print(f"Executed Quantity: {result['executed_quantity']:.8f}")
    print(f"Price: ${result['price']}")
    print(f"Number of Chunks: {result['num_chunks']}")
    print(f"Interval: {result['interval_seconds']} seconds")
    print(f"\nOrder IDs: {result['order_ids']}")
    print(f"Status: {result['status']}")
    print("="*70 + "\n")


def main():
    try:
        # Usage: python twap.py <SYMBOL> <BUY/SELL> <TOTAL_QTY> <PRICE> <NUM_CHUNKS> <INTERVAL_SECONDS> [--dry-run]
        if len(sys.argv) < 7:
            raise ValueError(
                "Usage: python twap.py <SYMBOL> <BUY/SELL> <TOTAL_QTY> "
                "<PRICE> <NUM_CHUNKS> <INTERVAL_SECONDS> [--dry-run]"
            )

        symbol = sys.argv[1].upper()
        side = sys.argv[2].upper()
        total_quantity = float(sys.argv[3])
        price = float(sys.argv[4])
        num_chunks = int(sys.argv[5])
        interval_seconds = int(sys.argv[6])
        dry_run = "--dry-run" in sys.argv

        validate_twap_inputs(symbol, side, total_quantity, price, num_chunks, interval_seconds)

        result = place_twap_order(
            symbol, side, total_quantity, price, num_chunks, interval_seconds, dry_run
        )

        print_twap_result(result)

    except Exception as e:
        logger.error(f"TWAP order failed: {str(e)}")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
