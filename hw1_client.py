import socket
from clientFile.mainProcess_client import *


hostAddress = ("127.0.0.1", 9987)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(hostAddress)

main = MainProcess_Client()
main.mainProcess(clientSocket)
