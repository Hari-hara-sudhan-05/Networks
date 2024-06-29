from twisted.internet import protocol,reactor

class floodclient(protocol.Protocol):
    def connectionMade(self):
        graph={'A' :['B','C'],
               'B':['D','E'],
               'C':['E'],
               'D':['A'],
               'E':[]}
        print('the graph is :',graph)
        source=input("enter start vertex for flooding:")
        msg=input("enter msg:")
        dic={'graph':graph,'start':source,'msg':msg}
        self.transport.write(str(dic).encode())
    
    def dataReceived(self, data):
        print('server said:',data.decode())
    
class floodfactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return floodclient()

reactor.connectTCP("localhost", 8000, floodfactory())
reactor.run()