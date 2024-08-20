import quickfix as fix
import quickfix44 as fix44
import random

# Stock details
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

# Generate random orders
def generate_random_orders(num_orders):
    orders = []
    for _ in range(num_orders):
        stock = random.choice(stocks)
        order = {
            "ticker": stock["ticker"],
            "price": stock["price"],
            "quantity": random.randint(1, 100),
            "side": random.choice(["buy", "sell"])  # Randomly choose buy or sell
        }
        orders.append(order)
    return orders

class Application(fix.Application):
    def onCreate(self, sessionID):
        print(f"Session created: {sessionID}")
        self.sessionID = sessionID
        return

    def onLogon(self, sessionID):
        print(f"Logon - sessionID: {sessionID}")

        # Generate 1000 random orders
        orders = generate_random_orders(1000)

        # Send each order to the server
        for order in orders:
            self.send_new_order_single(sessionID, order)

    def onLogout(self, sessionID):
        print(f"Logout - sessionID: {sessionID}")
        return

    def toAdmin(self, message, sessionID):
        print(f"Admin message sent: {message}")
        return

    def fromAdmin(self, message, sessionID):
        print(f"Admin message received: {message}")
        return

    def toApp(self, message, sessionID):
        print(f"Application message sent: {message}")
        return

    def fromApp(self, message, sessionID):
        print(f"Application message received: {message}")
        return

    def send_new_order_single(self, sessionID, order):
        side = fix.Side_BUY if order["side"] == "buy" else fix.Side_SELL

        # Create a NewOrderSingle message
        new_order = fix44.NewOrderSingle()

        # Set fields for the NewOrderSingle message
        new_order.setField(fix.ClOrdID(str(random.randint(1000, 9999))))  # Unique order ID
        new_order.setField(fix.HandlInst(fix.HandlInst_MANUAL_ORDER_BEST_EXECUTION))
        new_order.setField(fix.Symbol(order["ticker"]))
        new_order.setField(fix.Side(side))
        new_order.setField(fix.TransactTime())
        new_order.setField(fix.OrdType(fix.OrdType_LIMIT))  # Set as a limit order

        # Set price and quantity
        new_order.setField(fix.Price(order["price"]))
        new_order.setField(fix.OrderQty(order["quantity"]))

        # Send the message
        fix.Session.sendToTarget(new_order, sessionID)
        print(f"Sent {order['side']} order: {order}")


def main():
    settings = fix.SessionSettings("config/client.cfg")
    application = Application()
    store_factory = fix.FileStoreFactory(settings)
    log_factory = fix.FileLogFactory(settings)
    initiator = fix.SocketInitiator(application, store_factory, settings, log_factory)
    
    print("Starting client...")
    initiator.start()
    input("Press <ENTER> to stop the client...\n")
    initiator.stop()

if __name__ == "__main__":
    main()
