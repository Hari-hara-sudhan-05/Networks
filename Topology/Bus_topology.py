class DropLink(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.name = None

    def connectionMade(self):
        self.factory.clients.append(self)
        print("New client connected to bus backbone.")

    def connectionLost(self, reason):
        self.factory.clients.remove(self)
        print("Client disconnected.")

    def dataReceived(self, data):
        message = data.decode().strip()

        if not self.name:
            self.name = message
            print(f"{self.name} connected to bus.")
        else:
            if message.startswith("@"):
                recipient, private_message = message[1:].split(":", 1)
                self.sendPrivateMessage(recipient, private_message)
            else:
                print(f"{self.name}: {message}")
                self.broadcastMessage(f"{self.name}: {message}")

    def sendPrivateMessage(self, recipient, message):
        for client in self.factory.clients:
            if client.name == recipient:
                client.transport.write(f"(Private) {self.name}: {message}\n".encode())
                break
        else:
            self.transport.write(f"Error: User {recipient} not found.\n".encode())

    def broadcastMessage(self, message):
        for client in self.factory.clients:
            if client != self:
                client.transport.write(f"{message}\n".encode())

class BusBackbone(protocol.Factory):
    def __init__(self):
        self.clients = []

    def buildProtocol(self, addr):
        return DropLink(self)

if __name__ == "__main__":
    reactor.listenTCP(8000, BusBackbone())
    print("Bus server started.")
    print("Enter your name as first message to register. To send a message to a particular username use '@username: message'.")
    reactor.run()