from twisted.internet import reactor, protocol

class FileTransferClientProtocol(protocol.Protocol):
	def connectionMade(self):
		f=open("myfile.txt", 'rb')
		self.fileData = f.read()
		self.transport.write(b"SEND")

	def dataReceived(self, data):
		if data == b"READY":
			self.transport.write(self.fileData)

		elif data == b"RECEIVED":
			print("File transfer complete.")
			self.transport.loseConnection()

		else:
			print("Error:", data.decode())
			self.transport.loseConnection()

class FileTransferClientFactory(protocol.ClientFactory):
	protocol = FileTransferClientProtocol

if __name__ == "__main__":
	reactor.connectTCP("localhost", 7000, FileTransferClientFactory())
	reactor.run()	

