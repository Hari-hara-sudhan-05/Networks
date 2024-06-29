from twisted.internet import protocol, reactor


class RingTopolgy(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.name = None
    
    def connectionMade(self):
        print('new client connected', self.transport.getPeer())
        self.factory.clients.append(self)
    
    def connectionLost(self, reason):
        index = self.factory.clients.index(self)
        self.factory.clients[index] = None
    
    def dataReceived(self, data):
        msg = data.decode().strip()
        if not self.name:
            self.name = msg
            print(f'{self.name} has connected to the server')
            self.factory.names.append(self.name)
        
        else:
            if msg.startswith('@'):
                receipt, pvt_msg = msg[1:].split(':', 1)
                receiver_index = self.factory.names.index(receipt)
                sender_index = self.factory.names.index(self.name)
                
                while sender_index != receiver_index:
                    sender_index += 1
                    if sender_index == len(self.factory.names):
                        sender_index = 0
                    
                    if self.factory.client[sender_index] is None:
                        self.transport.write('link failure'.encode())
                        break
                
                self.sendPrivateMessage(self.factory.names[sender_index], pvt_msg)
            
            else:
                self.transport.write(msg.encode())
    
    def sendPrivateMessage(self, receipt, msg):
        for client in self.factory.clients:
            if client is not None:
                if client == receipt:
                    client.transport.write(f"{self.name} : {msg}".encode())
                    break
        else:
            self.transport.write(f"Error : {receipt} not found\n".encode())


class RingFactory(protocol.Factory):
    def __init__(self):
        self.clients = []
        self.names = []
    
    def buildProtocol(self, addr):
        return RingTopolgy(self)


reactor.listenTCP(8080, RingFactory())
print('server started Listening on port 8080..')
print('''Enter client name to register. Enter @ before the starting of a message to send message to another client.''')
reactor.run()