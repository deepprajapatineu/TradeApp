import quickfix as fix
from .order_generator import OrderGenerator
from .order_sender import OrderSender

class Application(fix.Application):
    def onCreate(self, sessionID):
        print(f"Session created: {sessionID}")
        self.sessionID = sessionID

    def onLogon(self, sessionID):
        print(f"Logon - sessionID: {sessionID}")
        orders = OrderGenerator.generate_random_orders(1000)
        for order in orders:
            OrderSender.send_new_order_single(sessionID, order)
        OrderSender.send_order_cancel_request(sessionID, orders[0])

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
