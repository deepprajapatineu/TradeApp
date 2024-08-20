import random

class OrderGenerator:
    stocks = [
        {"ticker": "AAPL", "price": 150.00},
        {"ticker": "GOOG", "price": 2800.00},
        {"ticker": "TSLA", "price": 700.00},
        {"ticker": "AMZN", "price": 3400.00},
        {"ticker": "MSFT", "price": 300.00},
        {"ticker": "FB", "price": 350.00},
        {"ticker": "NFLX", "price": 550.00},
        {"ticker": "NVDA", "price": 220.00},
    ]

    @staticmethod
    def generate_random_orders(num_orders):
        orders = []
        for _ in range(num_orders):
            stock = random.choice(OrderGenerator.stocks)
            order = {
                "ticker": stock["ticker"],
                "price": stock["price"],
                "quantity": random.randint(1, 100),
                "side": random.choice(["buy", "sell"])
            }
            orders.append(order)
        return orders
