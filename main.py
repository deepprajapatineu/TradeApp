import quickfix as fix
from src.client.application import Application as ClientApplication
from src.server.application import Application as ServerApplication

def start_client():
    settings = fix.SessionSettings("config/client.cfg")
    application = ClientApplication()
    store_factory = fix.FileStoreFactory(settings)
    log_factory = fix.FileLogFactory(settings)
    initiator = fix.SocketInitiator(application, store_factory, settings, log_factory)

    print("Starting client...")
    initiator.start()
    input("Press <ENTER> to stop the client...\n")
    initiator.stop()

def start_server():
    settings = fix.SessionSettings("config/server.cfg")
    application = ServerApplication()
    store_factory = fix.FileStoreFactory(settings)
    log_factory = fix.FileLogFactory(settings)
    acceptor = fix.SocketAcceptor(application, store_factory, settings, log_factory)

    print("Starting server...")
    acceptor.start()
    input("Press <ENTER> to stop the server...\n")
    acceptor.stop()

if __name__ == "__main__":
    choice = input("Start client or server? (c/s): ").strip().lower()
    if choice == 'c':
        start_client()
    elif choice == 's':
        start_server()
    else:
        print("Invalid choice.")
