from twisted.internet import reactor, protocol

class StopAndWaitClient(protocol.Protocol):

    def connectionMade(self):
        self.sendData()

    def sendData(self):
        if self.transport.connected:
            data = input("Enter data/quit to Server: ")
            if data == 'q':
                self.transport.write(data.encode())
                self.transport.loseConnection()
                return
            self.transport.write(data.encode())
            self.timeout = reactor.callLater(7, self.resendData)

    def resendData(self):
        print("Timeout, Rend the Data.")
        if self.transport.connected:
            self.sendData()

    def dataReceived(self, data):
        print("Acknowledge from Server -", data.decode())
        if self.timeout.active():
            self.timeout.cancel()
        self.sendData()

class StopAndWaitClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return StopAndWaitClient()

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed.")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost.")
        reactor.stop()

reactor.connectTCP('localhost', 8081, StopAndWaitClientFactory())
reactor.run()

# SLIDING WINDOW


from twisted.internet import reactor, protocol
from twisted.internet.interfaces import IAddress


class SlidingWindow(protocol.Protocol):
    def __init__(self):
        self.packets = [
            b'packet 0',
            b'packet 1',
            b'packet 2',
            b'packet 3',
            b'packet 4',
            b'packet 5',
        ]
        self.base = 0
        self.ack_num = 0
    
    def connectionMade(self):
        self.sendData()
    
    def sendData(self):
        if self.base < len(self.packets):
            self.transport.write(self.packets[self.ack_num])
            self.ack_num += 1
            self.timeout = reactor.callLater(7, self.resend)
    
    def resend(self):
        print('Timed out , resending')
        self.ack_num = self.base
        self.sendData()
    
    def dataReceived(self, data):
        print('Acknowledge from Server -', data.decode())
        if self.timeout.active():
            self.timeout.cancel()
        self.base += 1
        if self.base < len(self.packets):
            self.sendData()


class SlidindFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return SlidingWindow()


reactor.connectTCP('localhost', 8000, SlidindFactory())
reactor.run()
