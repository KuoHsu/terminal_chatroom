import socket
import clientFile.mainProcess_client as main


hostAddress = ("127.0.0.1", 9987)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(hostAddress)

main.mainProcess(clientSocket)
