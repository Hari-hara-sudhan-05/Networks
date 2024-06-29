from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
class ChatServer(DatagramProtocol):
    def __init__(self):
        self.users = {}

    def datagramReceived(self, data, addr):
        message = data.decode().strip()
        if addr in self.users:
            username = self.users[addr]
            message = f"<{username}> {message} \n"
            for user_addr in self.users:
                if user_addr != addr:
                    self.transport.write(message.encode(), user_addr)
        else:
            self.users[addr] = message.split()[0]
            self.transport.write(b"Welcome to the chat!\n", addr)
if __name__ == "__main__":
    reactor.listenUDP(5000, ChatServer())
    print("Server started.")
    reactor.run()

