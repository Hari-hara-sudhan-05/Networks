import pickle
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class FTClient(DatagramProtocol):

    def startProtocol(self):
        self.transport.connect('127.0.0.1', 1234)
        self.sendDatagram()
    
    def sendDatagram(self):
        file_name = input('Enter file name to send : ')
        file = open(f'{file_name}','r')
        file_data = file.read()
        data = (file_name,file_data)
        if file_name :
            self.transport.write(pickle.dumps(data)) 
        else:
            reactor.stop()

    def datagramReceived(self, datagram, host):
        print('Datagram received: ', repr(datagram))
        self.sendDatagram()
        

def main():
    protocol = FTClient()
    t = reactor.listenUDP(0, protocol)
    reactor.run()

if __name__ == '__main__':
    main()


