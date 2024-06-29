from twisted.internet import reactor, protocol
 
class Client(protocol.Protocol): 
    def connectionMade(self): 
        print("Making Connection with the Server...") 
        self.transport.write('Hello Server!'.encode()) 
        self.transport.loseConnection() 
        
class clientFact(protocol.ClientFactory): 
    def buildProtocol(self, addr): 
        return Client() 

if __name__ == "__main__": 
    reactor.connectTCP("localhost", 8000, clientFact()) 
    reactor.run()