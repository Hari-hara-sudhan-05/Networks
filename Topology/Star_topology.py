from twisted.internet import protocol, reactor


class StartTopology(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.name = None
    
    def connectionMade(self):
        print('new Client connected', self.transport.getPeer())
        self.factory.clients.append(self)
    
    def connectionLost(self, addr):
        self.factory.clients.remove(self)
    
    def dataReceived(self, data):
        message = data.decode().strip()
        if not self.name:
            self.name = message
        
        else:
            if message.startwith('@'):
                reciptent, private_message = message[1:].split(':', 1)
                self.sendThroughServer(reciptent, private_message)
            else:
                self.transport.write(message)
    
    def sendThroughServer(self, receiptent, message):
        self.transport.write(message)
        self.sendPrivateMessage(receiptent, message)
    
    def sendPrivateMessage(self, receiptent, message):
        for client in self.factory.clients:
            if client.name == receiptent:
                client.transport.write(message.encode())
                break
        else:
            self.transport.write('error'.encode())


class StarFactory(protocol.Factory):
    def __init__(self):
        self.clients = []
    
    def buildProtocol(self, addr):
        return StartTopology()


if __name__ == '__main__':
    reactor.listenTCP(8080, StarFactory())
    reactor.run()