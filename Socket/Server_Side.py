import socket
server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_address=('localhost',1444)
server_socket.bind(server_address)
server_socket.listen(2)
while True:
    print("Waiting for making connection")
    connection,client_address=server_socket.accept()
    print("Client address:",client_address)

    data=connection.recv(1024)
    print("Received:",data.decode())

    if data:
        connection.sendall(data)
    else:
        print("No data received")

    connection.close()

