import sys
from config import client

from logger import logger
# from config import client   # Uncomment when live API is available


def validate_inputs(symbol: str, side: str, quantity: float, price: float):
    if not symbol.isalnum():
        raise ValueError("Invalid symbol format")

    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be BUY or SELL")

    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0")

    if price <= 0:
        raise ValueError("Price must be greater than 0")


def place_limit_order(symbol: str, side: str, quantity: float, price: float):
    logger.info(
        f"Placing LIMIT order | {symbol} | {side} | qty={quantity} | price={price}"
    )


    order = client.futures_create_order(
        symbol=symbol,
        side=side,
        type="LIMIT",
        quantity=quantity,
        price=price,
        timeInForce="GTC"
    )

    order_id = order.get('orderId') or order.get('id')
    logger.info(f"Limit order placed successfully | Order ID: {order_id}")
    return order


def main():
    try:
        # Expecting: symbol side quantity price
        if len(sys.argv) != 5:
            raise ValueError(
                "Usage: python limit_orders.py <SYMBOL> <BUY/SELL> <QUANTITY> <PRICE>"
            )

        symbol = sys.argv[1].upper()
        side = sys.argv[2].upper()
        quantity = float(sys.argv[3])
        price = float(sys.argv[4])

        validate_inputs(symbol, side, quantity, price)
        place_limit_order(symbol, side, quantity, price)

    except Exception as e:
        logger.error(f"Limit order failed: {str(e)}")
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
