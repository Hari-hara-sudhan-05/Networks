from twisted.internet import reactor, protocol

class RARPServer(protocol.Protocol):
    def connectionMade(self):
        print("client connected")

    def dataReceived(self, data):
        global RARP_tabel
        packet = data.decode().split('/',4)
        if packet[2] in RARP_tabel:
            newData = f"{packet[2]}/{RRARP_tabel[packet[2]]}/{packet[0]}/{packet[1]}"
            self.transport.write(newData.encode())
        
        else:
            self.transport.write('no mac found'.encode())
        
    def connectionLost(self, reason):
        print("client removed")
        return


class RRARPServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return RRARPServer()


RRARP_tabel = {}
RRARP_tabel['00:11:22:33:44:55'] = '192.168.1.1'

reactor.listenTCP(1234, RRARPServerFactory())
reactor.run()
