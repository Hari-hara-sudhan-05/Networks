from twisted.internet import reactor 
from twisted.internet.protocol import Protocol, Factory, connectionDone 
from twisted.python.failure import Failure 

class Server(Protocol): 
    def connectionMade(self): 
        peer = self.transport.getPeer() 
        print("A node has made connection :", peer.host, peer.port) 
        
    def dataReceived(self, data: bytes) -> None: 
        print("Data Received from the node :", data.decode()) 
    
    def connectionLost(self, reason: Failure = ...) -> None: 
        print("Connection from a Node is Lost...") 
        
if __name__ == "__main__": 
    ServerFactory = Factory() 
    ServerFactory.protocol = Server 
    reactor.listenTCP(8000, ServerFactory) 
    print("Server has been hosted at port 8000...") 
    reactor.run()