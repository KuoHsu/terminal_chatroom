import random
import User_server


class UserPool_server():

    def __init__(self):
        self.userList = {}
        self.uidList = []
        self.userCount = 0

    def __getNewUID__(self):
        newUID = ""
        for i in range(0, 8):
            newUID += str(random.randint(0, 9))

        while newUID in uidList:
            newUID = ""
            for i in range(0, 8):
                newUID += str(random.randint(0, 9))

        self.uidList.append(newUID)
        return newUID

    def newUser(self, socket, name):
        nUID = __getNewUID__()
        nUser = User_server(socket, nUID, name)
        self.userList[nUID] = nUser
        self.userCount += 1
        return nUser

    def getUser(self, UID):
        return self.userList[UID]

    def removeUser(self, UID):
        del self.userList[UID]
        self.uidList.remove(UID)
        self.userCount -= 1
