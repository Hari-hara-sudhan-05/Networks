from twisted.internet import reactor, protocol
import pickle

class NetworkGraph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, node1, node2, cost):
        if node1 not in self.graph:
            self.graph[node1] = []
        self.graph[node1].append((node2, cost))
        
        if node2 not in self.graph:
            self.graph[node2] = []
        self.graph[node2].append((node1, cost))

class ClientProtocol(protocol.Protocol):
    def connectionMade(self):
        print("Connection Made!")
        # Create a network graph
        network = NetworkGraph()
        network.add_edge('A', 'B', 10)
        network.add_edge('A', 'C', 3)
        network.add_edge('B', 'C', 1)
        network.add_edge('B', 'D', 2)
        network.add_edge('C', 'D', 8)
        network.add_edge('C', 'E', 2)
        network.add_edge('D', 'E', 7)

        # Serialize and send the network graph to the server
        data = pickle.dumps(network)
        self.transport.write(data)
        print('Sent network graph to server')

    def dataReceived(self, data):
        shortest_paths = pickle.loads(data)
        print('Received shortest paths from server:', shortest_paths)
        reactor.stop()

class ClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return ClientProtocol()

if __name__ == "__main__":
    reactor.connectTCP("localhost", 8000, ClientFactory())
    reactor.run()
