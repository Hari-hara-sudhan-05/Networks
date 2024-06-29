# from typing import Optional
from twisted.internet import reactor,protocol
class echoserver(protocol.Protocol):

    def connectionMade(self):
        print('client connected')

    def dataReceived(self, data):
        recv=eval(data.decode())
        graph=recv.get('graph')
        start=recv.get('start')
        msg=recv.get('msg')
        connected=self.find_connected_edges(graph,start)
        for i in connected:
            print(f'message sent to {i} is {msg}')
        self.transport.write(f'msg sent'.encode())
        self.transport.loseConnection()
    
    def find_connected_edges(self, graph, start):
        if start not in graph:
            return []
        
        connected = []
        connected.append(start)
        connected.extend(graph[start])
        for i in connected:
            if graph[i] is not None:
                for j in graph[i]:
                    if j not in connected:
                        connected.append(j)
        
        connected.remove(start)
        
        return connected


class echofactory(protocol.Factory):
    def buildProtocol(self, addr):
        return echoserver()

if __name__=='__main__':
    reactor.listenTCP(8000,echofactory())
    reactor.run()