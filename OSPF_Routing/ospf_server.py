from twisted.internet import reactor, protocol
import pickle
import heapq

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

    def shortest_path(self, start):
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0
        visited = set()
        queue = [(0, start)]

        while queue:
            current_distance, current_node = heapq.heappop(queue)

            if current_node in visited:
                continue
            visited.add(current_node)

            for neighbor, cost in self.graph[current_node]:
                distance = current_distance + cost
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(queue, (distance, neighbor))

        return distances

class OSPFProtocol(protocol.Protocol):
    def __init__(self):
        self.graph = None
    
    def dataReceived(self, data):
        self.graph = pickle.loads(data)
        print('Received network graph from client:', self.graph)

        shortest_paths = {}
        for node in self.graph.graph:
            shortest_paths[node] = self.graph.shortest_path(node)

        response = pickle.dumps(shortest_paths)
        self.transport.write(response)
        print('Sent shortest paths back to client')

class OSPFFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return OSPFProtocol()
    
if __name__ == "__main__":
    reactor.listenTCP(8000, OSPFFactory())
    print('Server started...')
    reactor.run()
