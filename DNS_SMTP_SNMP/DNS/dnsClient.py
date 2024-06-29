from twisted.internet import reactor,protocol

class dns_client(protocol.Protocol):

    def connectionMade(self):
        print("connected to server..")
        a=input("enter domain name:")
        self.transport.write(a.encode())

    def dataReceived(self, data):
        d=data.decode()
        if d is not None:
            print(data)
        else:
            print("invalid domain name")
            
class dns_client_factory(protocol.ClientFactory):

    def buildProtocol(self, addr):
        return dns_client()
    
reactor.connectTCP('localhost',8002,dns_client_factory())
reactor.run()