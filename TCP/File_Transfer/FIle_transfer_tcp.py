
from twisted.internet import reactor, protocol

class FileTransferProtocol(protocol.Protocol):
	def connectionMade(self):
		print("Client connected.")

	def dataReceived(self, data):
		if data == b"SEND":
			self.transport.write(b"READY")
			self.transferFile = True
		
		elif self.transferFile:
			with open("../../../TCP/TCP/received_file", "wb") as f:
				f.write(data)
			self.transport.write(b"RECEIVED")
			self.transferFile = False

		else:
			self.transport.write(b"ERROR")

class FileTransferFactory(protocol.Factory):
	def buildProtocol(self, addr):
		return FileTransferProtocol()

if __name__ == "__main__":
	reactor.listenTCP(7000, FileTransferFactory())
	print("Server started.")
	reactor.run()



