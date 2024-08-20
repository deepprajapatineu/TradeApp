import quickfix as fix
import quickfix44 as fix44
import random

class OrderSender:
    @staticmethod
    def send_new_order_single(sessionID, order):
        side = fix.Side_BUY if order["side"] == "buy" else fix.Side_SELL
        new_order = fix44.NewOrderSingle()
        new_order.setField(fix.ClOrdID(str(random.randint(1000, 9999))))
        new_order.setField(fix.HandlInst(fix.HandlInst_MANUAL_ORDER_BEST_EXECUTION))
        new_order.setField(fix.Symbol(order["ticker"]))
        new_order.setField(fix.Side(side))
        new_order.setField(fix.TransactTime())
        new_order.setField(fix.OrdType(fix.OrdType_LIMIT))
        new_order.setField(fix.Price(order["price"]))
        new_order.setField(fix.OrderQty(order["quantity"]))
        fix.Session.sendToTarget(new_order, sessionID)
        print(f"Sent {order['side']} order: {order}")

    @staticmethod
    def send_order_cancel_request(sessionID, order):
        side = fix.Side_BUY if order["side"] == "buy" else fix.Side_SELL
        cancel_request = fix44.OrderCancelRequest()
        cancel_request.setField(fix.OrigClOrdID(str(random.randint(1000, 9999))))
        cancel_request.setField(fix.ClOrdID(str(random.randint(1000, 9999))))
        cancel_request.setField(fix.Symbol(order["ticker"]))
        cancel_request.setField(fix.Side(side))
        cancel_request.setField(fix.TransactTime())
        fix.Session.sendToTarget(cancel_request, sessionID)
        print(f"Sent cancel request for {order['side']} order: {order}")
