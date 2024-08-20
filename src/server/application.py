import quickfix as fix
from .message_handler import MessageHandler

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
        msg_type = fix.MsgType()
        message.getHeader().getField(msg_type)
        if msg_type.getValue() == fix.MsgType_NewOrderSingle:
            MessageHandler.handle_new_order_single(message, sessionID)
        elif msg_type.getValue() == fix.MsgType_OrderCancelRequest:
            MessageHandler.handle_order_cancel_request(message, sessionID)
        elif msg_type.getValue() == fix.MsgType_OrderCancelReplaceRequest:
            MessageHandler.handle_order_cancel_replace_request(message, sessionID)
