import socket


class User_client:

    def __init__(self, socket, name, uid):
        self.socket = socket
        self.name = name
        self.uid = uid

    def send(self, _type, action, content):
        msg = {}
        msg["type"] = _type
        msg["action"] = action
        msg["content"] = content
        emsg = str(msg).encode("UTF-8")
        self.socket.send(emsg)

    def getMsg(self):
        msg = self.socket.recv(2048).decode("UTF-8")
        message = eval(msg)
        return message

    def getName(self):
        return self.name

    def getUID(self):
        return self.uid

    def close(self):
        self.socket.close()
