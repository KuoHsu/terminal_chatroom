import socket
import threading
from serverFile.mainProcess_server import *

hostAddress = ("127.0.0.1", 9987)

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(("127.0.0.1", 9987))
serverSocket.listen(100)
main = MainProcess_server()
print("伺服器成功啟動")
while True:
    newConnect, addr = serverSocket.accept()
    newThread = threading.Thread(
        target=main.mainProcess, args=(newConnect, addr,))
    newThread.start()
