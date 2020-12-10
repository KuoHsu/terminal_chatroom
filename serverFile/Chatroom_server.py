from serverFile.UserPool_server import *
from serverFile.ChatroomPool_server import *
# 個別聊天室內部使用者管理
# 0. 以隨機6碼由大寫英文、數字組合成之ID與指定名稱建立
# 1. 加入使用者
# 2. 使用者離開
# 3. 接收使用者發言
# 4. 聊天室內部訊息廣播
# 5. 向指定使用者傳遞特定訊息
# 6. 更動聊天室設定
# 8. 取得聊天室資訊


class Chatroom_server:

    def __init__(self, CID, name, managePool):
        self.CID = CID
        self.name = name
        self.managePool = managePool
        self.members = {}
        self.memberCount = 0

    def newMember(self, user: User_server):
        self.members[user.UID] = user
        self.memberCount += 1
        msg = user.getName() + " 加入了聊天室！"
        exu = user.getUID()
        self.__innerBroadcast__(msg, [exu])
        return True

    def memberLeave(self, user: User_server):
        msg = user.getName() + " 已離開聊天室。"
        uid = user.getUID()
        del self.members[uid]
        self.memberCount -= 1
        self.__innerBroadcast__(msg, [])
        if self.memberCount == 0:
            self.__close__()
        return True

    def memberMessage(self, user: User_server, msg):
        message = user.getName() + ": " + msg
        exu = user.getUID()
        self.__innerBroadcast__(message, [exu])

    def __innerBroadcast__(self, msg, excludingUser):
        for uid in self.members:
            if uid not in excludingUser:
                self.members[uid].send('chatroom', 'msg', msg)

    def __assignSend__(self, receiver: User_server, msg):
        uid = receiver.getUID()
        _receiver = self.members[uid]
        _receiver.send('chatroom', 'msg', msg)

    def getChatroomInfo(self):
        msg = " 編號: %s | 室名: %s | 人數: %d" % (
            self.CID, self.name, self.memberCount)
        return msg

    def getCID(self):
        return self.CID

    def __close__(self):
        self.managePool.chatroomClose(self.CID)
