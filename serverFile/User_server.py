# 取得資訊
# 傳送訊息
import socket


class User_server:

    def __init__(self, socket, uid, name):
        self.socket = socket
        self.UID = uid
        self.name = name

    def send(self, _type, action, content):
        msg = {}
        msg["type"] = _type
        msg["action"] = action
        msg["content"] = content
        message = str(msg).encode("UTF-8")
        self.socket.send(message)

    def getMessage(self):
        try:
            msg = self.socket.recv(2048).decode("UTF-8")
            message = eval(msg)
            return message
        except ConnectionResetError as e:
            raise

    def getUID(self):
        return self.UID

    def getName(self):
        return self.name

    def disconnect(self):
        self.socket.close()
