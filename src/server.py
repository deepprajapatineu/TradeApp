import quickfix as fix
import quickfix44 as fix44

class Application(fix.Application):
    def onCreate(self, sessionID):
        print(f"Session created: {sessionID}")
        self.sessionID = sessionID

    def onLogon(self, sessionID):
        print(f"Logon - sessionID: {sessionID}")

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
        msg_type = fix.MsgType()
        message.getHeader().getField(msg_type)

        if msg_type.getValue() == fix.MsgType_NewOrderSingle:
            self.on_new_order_single(message, sessionID)
        elif msg_type.getValue() == fix.MsgType_OrderCancelRequest:
            self.on_order_cancel_request(message, sessionID)
        elif msg_type.getValue() == fix.MsgType_OrderCancelReplaceRequest:
            self.on_order_cancel_replace_request(message, sessionID)

    def on_new_order_single(self, message, sessionID):
        symbol = fix.Symbol()
        side = fix.Side()
        order_qty = fix.OrderQty()
        price = fix.Price()

        message.getField(symbol)
        message.getField(side)
        message.getField(order_qty)
        message.getField(price)

        print(f"Received NewOrderSingle: {symbol.getValue()} {order_qty.getValue()} @ {price.getValue()} {side.getValue()}")

        # Respond with an ExecutionReport (accepted)
        exec_report = fix44.ExecutionReport(
            fix.OrderID(str(random.randint(1000, 9999))),
            fix.ExecID(str(random.randint(1000, 9999))),
            fix.ExecType(fix.ExecType_FILL),
            fix.OrdStatus(fix.OrdStatus_FILLED),
            symbol,
            side,
            fix.LeavesQty(0),
            fix.CumQty(order_qty.getValue()),
            fix.AvgPx(price.getValue())
        )
        exec_report.setField(fix.ClOrdID(message.getField(fix.ClOrdID()).getValue()))
        fix.Session.sendToTarget(exec_report, sessionID)

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
    settings = fix.SessionSettings("config/server.cfg")
    application = Application()
    store_factory = fix.FileStoreFactory(settings)
    log_factory = fix.FileLogFactory(settings)
    acceptor = fix.SocketAcceptor(application, store_factory, settings, log_factory)

    print("Starting server...")
    acceptor.start()
    input("Press <ENTER> to stop the server...\n")
    acceptor.stop()

if __name__ == "__main__":
    main()
