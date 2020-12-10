import socket
import threading
import mainProcess_server

hostAddress = ("127.0.0.1", 9987)

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(hostAddress)
while True:
    newConnect, addr = serverSocket.accept()
    newThread = threading.Thread(
        target=mainProcess_server.mainProcess, args=(newConnect, addr,))
    newThread.start()
