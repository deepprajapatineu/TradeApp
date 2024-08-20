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

    def onLogon(self, sessionID):
        print(f"Logon - sessionID: {sessionID}")

        # Generate 1000 random orders
        orders = generate_random_orders(1000)

        # Send each order to the server
        for order in orders:
            self.send_new_order_single(sessionID, order)

        # Send an Order Cancel Request for the first order
        self.send_order_cancel_request(sessionID, orders[0])

    def onLogout(self, sessionID):
        print(f"Logout - sessionID: {sessionID}")

    def toAdmin(self, message, sessionID):
        print(f"Admin message sent: {message}")

    def fromAdmin(self, message, sessionID):
        print(f"Admin message received: {message}")

    def toApp(self, message, sessionID):
        print(f"Application message sent: {message}")

    def fromApp(self, message, sessionID):
        print(f"Application message received: {message}")

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

    def send_order_cancel_request(self, sessionID, order):
        side = fix.Side_BUY if order["side"] == "buy" else fix.Side_SELL

        # Create an OrderCancelRequest message
        cancel_request = fix44.OrderCancelRequest()

        # Set fields for the OrderCancelRequest message
        cancel_request.setField(fix.OrigClOrdID(str(random.randint(1000, 9999))))
        cancel_request.setField(fix.ClOrdID(str(random.randint(1000, 9999))))
        cancel_request.setField(fix.Symbol(order["ticker"]))
        cancel_request.setField(fix.Side(side))
        cancel_request.setField(fix.TransactTime())

        # Send the cancel request message
        fix.Session.sendToTarget(cancel_request, sessionID)
        print(f"Sent cancel request for {order['side']} order: {order}")


    def on_order_cancel_request(self, message, sessionID):
        orig_cl_ord_id = fix.OrigClOrdID()
        cl_ord_id = fix.ClOrdID()
        symbol = fix.Symbol()
        side = fix.Side()

        message.getField(orig_cl_ord_id)
        message.getField(cl_ord_id)
        message.getField(symbol)
        message.getField(side)

        print(f"Received OrderCancelRequest: Cancel {orig_cl_ord_id.getValue()} for {symbol.getValue()} {side.getValue()}")

        # Respond with a Cancel ExecutionReport
        exec_report = fix44.ExecutionReport(
            fix.OrderID(orig_cl_ord_id.getValue()),
            fix.ExecID(str(random.randint(1000, 9999))),
            fix.ExecType(fix.ExecType_CANCELED),
            fix.OrdStatus(fix.OrdStatus_CANCELED),
            symbol,
            side,
            fix.LeavesQty(0),
            fix.CumQty(0),
            fix.AvgPx(0)
        )
        exec_report.setField(fix.ClOrdID(cl_ord_id.getValue()))
        fix.Session.sendToTarget(exec_report, sessionID)

    def on_order_cancel_replace_request(self, message, sessionID):
        orig_cl_ord_id = fix.OrigClOrdID()
        cl_ord_id = fix.ClOrdID()
        symbol = fix.Symbol()
        side = fix.Side()
        price = fix.Price()
        order_qty = fix.OrderQty()

        message.getField(orig_cl_ord_id)
        message.getField(cl_ord_id)
        message.getField(symbol)
        message.getField(side)
        message.getField(price)
        message.getField(order_qty)

        print(f"Received OrderCancelReplaceRequest: Modify {orig_cl_ord_id.getValue()} for {symbol.getValue()} {side.getValue()} to {order_qty.getValue()} @ {price.getValue()}")

        # Respond with a Replace ExecutionReport
        exec_report = fix44.ExecutionReport(
            fix.OrderID(orig_cl_ord_id.getValue()),
            fix.ExecID(str(random.randint(1000, 9999))),
            fix.ExecType(fix.ExecType_REPLACE),
            fix.OrdStatus(fix.OrdStatus_REPLACED),
            symbol,
            side,
            fix.LeavesQty(order_qty.getValue()),
            fix.CumQty(0),
            fix.AvgPx(price.getValue())
        )
        exec_report.setField(fix.ClOrdID(cl_ord_id.getValue()))
        fix.Session.sendToTarget(exec_report, sessionID)


def main():
    # Load the FIX configuration settings
    settings = fix.SessionSettings("config/client.cfg")

    # Create an application instance
    application = Application()

    # Create message store and log factories
    store_factory = fix.FileStoreFactory(settings)
    log_factory = fix.FileLogFactory(settings)

    # Initialize the initiator with the correct arguments
    initiator = fix.SocketInitiator(application, store_factory, settings, log_factory)

    print("Starting client...")
    initiator.start()
    input("Press <ENTER> to stop the client...\n")
    initiator.stop()

if __name__ == "__main__":
    main()
