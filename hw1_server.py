import socket
import threading
import serverFile.mainProcess_server as m

hostAddress = ("127.0.0.1", 9987)

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(("127.0.0.1", 9987))
serverSocket.listen(100)
print("伺服器成功啟動")
while True:
    newConnect, addr = serverSocket.accept()
    newThread = threading.Thread(
        target=m.mainProcess, args=(newConnect, addr,))
    newThread.start()
