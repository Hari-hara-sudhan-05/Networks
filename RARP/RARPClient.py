from twisted.internet import reactor, protocol


class RARPClient(protocol.Protocol):
    def connectionMade(self):
        a = input("Enter Mac address: ")
        packet = f"{'191.0.0.1'}/{'66:77:88:99:11:22'}/{a}/{'00:00:00:00:00:00'}"
        self.transport.write(packet.encode())
        

    def dataReceived(self, data):
        receives = data.decode()
        packet = receives.split('/', 4)
        if len(packet)==4:
            print('The ip address is',packet[1])
            self.transport.loseConnection()
        else:
            print(receives)
            self.transport.loseConnection()
        
        


class RARPClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return RARPClient()

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed.")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost.")
        reactor.stop()


reactor.connectTCP('localhost', 1234, RARPClientFactory())
reactor.run()
