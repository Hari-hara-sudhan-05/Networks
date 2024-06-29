from twisted.internet import reactor, protocol

class StopAndWaitServer(protocol.Protocol):
    def dataReceived(self, data):
        if data.decode() == "q":
            print("Client Disconnected!")
            self.transport.loseConnection()
        else:
            print("Message from Client -", data.decode())
            flag = str(input("Acknowledge or Not - "))
            if flag == "y":
                ack = f"ACK[{data.decode()}]"
                self.transport.write(ack.encode())

class StopAndWaitServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return StopAndWaitServer()

reactor.listenTCP(8081, StopAndWaitServerFactory())
reactor.run()



# SLIDING WINDOW

from twisted.internet import reactor, protocol
from twisted.internet.interfaces import IAddress


class SlidingServer(protocol.Protocol):
    expected_packet = 0
    s = False
    def dataReceived(self, data):
        packet_num = int(data.decode().split()[-1])
        
        if packet_num == 2 and self.s ==False:
            self.s = True
            print('break')
        elif packet_num == self.expected_packet:
            print('Received packet', packet_num)
            ack = str(packet_num)
            self.transport.write(ack.encode())
            self.expected_packet += 1
        else:
            print('Error')


class SlidingFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return SlidingServer()


reactor.listenTCP(8000, SlidingFactory())
reactor.run()