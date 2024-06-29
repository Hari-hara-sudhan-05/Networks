from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

class Chat(LineReceiver):

    def __init__(self, users):
        self.users = users
        self.name = None
        self.state = "GETNAME"

    def connectionMade(self):
        self.sendLine("What's your name?".encode())

    def connectionLost(self, reason):
        print(f'{self.name} disconnected !')
        if self.name in self.users:
            del self.users[self.name]

    def dataReceived(self, data):
        print(data)
        if self.state == "GETNAME":
            self.handle_GETNAME(data)
        else:
            print('chat')
            self.handle_CHAT(data)

    def handle_GETNAME(self, name):
        if name in self.users:
            self.sendLine("Name taken, please choose another.".encode())
            return
        self.sendLine(f"Welcome, {name.decode()}".encode())
        print(f'{name} is connected !')
        self.name = name
        self.users[name] = self
        self.state = "CHAT"

    def handle_CHAT(self, message):
        message = f'{self.name.decode()} : {message.decode()}'
        for name, protocol in self.users.items():
            if protocol != self:
                protocol.sendLine(message.encode())


class ChatFactory(Factory):

    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return Chat(self.users)

reactor.listenTCP(1234, ChatFactory())
reactor.run()