import sys

from config import client
from logger import logger


def validate_inputs(symbol: str, side: str, quantity: float):
    if not symbol.isalnum():
        raise ValueError("Invalid symbol format")

    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be BUY or SELL")

    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0")



def place_market_order(symbol: str, side: str, quantity: float):
    logger.info(f"Placing MARKET order | {symbol} | {side} | {quantity}")

    order = client.futures_create_order(
        symbol=symbol,
        side=side,
        type="MARKET",
        quantity=quantity
    )
    

    logger.info(f"Market order placed successfully | Order ID: {order.get('orderId')}")
    return order


def main():
    try:
        # Expecting: symbol side quantity
        if len(sys.argv) != 4:
            raise ValueError("Usage: python market_orders.py <SYMBOL> <BUY/SELL> <QUANTITY>")

        symbol = sys.argv[1].upper()
        side = sys.argv[2].upper()
        quantity = float(sys.argv[3])

        validate_inputs(symbol, side, quantity)

        place_market_order(symbol, side, quantity)

    except Exception as e:
        logger.error(f"Market order failed: {str(e)}")
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
