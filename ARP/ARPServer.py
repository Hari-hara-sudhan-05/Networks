from twisted.internet import reactor, protocol

class ARPServer(protocol.Protocol):
    def connectionMade(self):
        print("client connected")

    def dataReceived(self, data):
        global arp_tabel
        packet = data.decode().split('/',4)
        if packet[2] in arp_tabel:
            newData = f"{packet[2]}/{arp_tabel[packet[2]]}/{packet[0]}/{packet[1]}"
            self.transport.write(newData.encode())
        
        else:
            self.transport.write('no mac found'.encode())
        
    def connectionLost(self, reason):
        print("client removed")
        return


class ARPServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return ARPServer()


arp_tabel = {}
arp_tabel['192.168.1.1'] = '00:11:22:33:44:55'

reactor.listenTCP(1234, ARPServerFactory())
reactor.run()
