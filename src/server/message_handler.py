import quickfix as fix
import quickfix44 as fix44
import random

class MessageHandler:
    @staticmethod
    def handle_new_order_single(message, sessionID):
        symbol = fix.Symbol()
        side = fix.Side()
        order_qty = fix.OrderQty()
        price = fix.Price()

        message.getField(symbol)
        message.getField(side)
        message.getField(order_qty)
        message.getField(price)

        print(f"Received NewOrderSingle: {symbol.getValue()} {order_qty.getValue()} @ {price.getValue()} {side.getValue()}")

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

    @staticmethod
    def handle_order_cancel_request(message, sessionID):
        orig_cl_ord_id = fix.OrigClOrdID()
        cl_ord_id = fix.ClOrdID()
        symbol = fix.Symbol()
        side = fix.Side()

        message.getField(orig_cl_ord_id)
        message.getField(cl_ord_id)
        message.getField(symbol)
        message.getField(side)

        print(f"Received OrderCancelRequest: Cancel {orig_cl_ord_id.getValue()} for {symbol.getValue()} {side.getValue()}")

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

    @staticmethod
    def handle_order_cancel_replace_request(message, sessionID):
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
