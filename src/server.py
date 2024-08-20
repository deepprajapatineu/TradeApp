import quickfix as fix
import quickfix44 as fix44

class Application(fix.Application):
    def onCreate(self, sessionID):
        print(f"Session created: {sessionID}")
        return

    def onLogon(self, sessionID):
        print(f"Logon - sessionID: {sessionID}")
        return

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
        self.onMessage(message, sessionID)
        return

    def onMessage(self, message, sessionID):
        msg_type = message.getHeader().getField(35)
        print(f"Message received: {message}")
        print(f"Message type: {msg_type}")

        if msg_type == "D":  # New Order Single
            cl_ord_id = message.getField(11)  # Client Order ID
            symbol = message.getField(55)  # Stock symbol
            side = message.getField(54)  # Buy or Sell
            order_qty = message.getField(38)  # Order quantity
            price = message.getField(44)  # Order price

            print(f"Received New Order Single - ClOrdID: {cl_ord_id}, Symbol: {symbol}, "
                  f"Side: {side}, OrderQty: {order_qty}, Price: {price}")

            # Respond with an Execution Report (FIX 4.4, MsgType = 8)
            execution_report = fix44.ExecutionReport(
                fix.OrderID("12345"),  # Order ID
                fix.ExecID("54321"),  # Execution ID
                fix.ExecType(fix.ExecType_FILL),  # Execution type
                fix.OrdStatus(fix.OrdStatus_FILLED),  # Order status
                fix.Symbol(symbol),  # Stock symbol
                fix.Side(side),  # Buy or Sell
                fix.LeavesQty(0),  # No remaining quantity
                fix.CumQty(order_qty),  # Filled quantity
                fix.AvgPx(price)  # Average price
            )
            execution_report.setField(fix.ClOrdID(cl_ord_id))  # Client Order ID

            fix.Session.sendToTarget(execution_report, sessionID)
            print(f"Execution Report sent: {execution_report}")
        return

def main():
    settings = fix.SessionSettings("config/server.cfg")
    application = Application()
    store_factory = fix.FileStoreFactory(settings)
    log_factory = fix.FileLogFactory(settings)
    acceptor = fix.SocketAcceptor(application, store_factory, settings, log_factory)
    acceptor.start()
    input("Press <ENTER> to stop the server...\n")
    acceptor.stop()

if __name__ == "__main__":
    main()
