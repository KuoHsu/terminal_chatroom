# 管理所有現存的聊天室
# 取得新聊天室ID
# 建立新聊天室
# 關閉聊天室事件
# 取得指定聊天室
# 取得聊天室列表
import random
from serverFile.Chatroom_server import *


class ChatroomPool_server:

    def __init__(self):
        super().__init__()
        self.CIDlist = []
        self.chatroomList = {}
        self.chatroomCount = 0

    def __getNewCID__(self):
        nCID = ""

        for i in range(0, 6):
            ac = random.randint(65, 90)
            nCID += chr(ac)
        while nCID in self.CIDlist:
            nCID = ""
            for i in range(0, 6):
                ac = random.randint(65, 90)
                nCID += chr(ac)

        self.CIDlist.append(nCID)
        return nCID

    def createNewChatroom(self, name):
        CID = self.__getNewCID__()
        newChatroom = Chatroom_server(CID, name, self)
        self.chatroomList[CID] = newChatroom
        return newChatroom

    def getChatroom(self, CID):
        if CID in self.CIDlist:
            return self.chatroomList[CID]
        else:
            return None

    def chatroomClose(self, CID):
        del self.chatroomList[CID]
        self.CIDlist.remove(CID)
        print("[聊天室 - %s]聊天室關閉了。" % CID)

    def getChatroomInfoList(self):
        msg = ""
        for cid in self.CIDlist:
            chatroom = self.chatroomList[cid]
            msg += chatroom.getChatroomInfo() + "\n"
        return msg

    def getChatroomIDList(self):
        chatIdList = []
        for cid in self.CIDlist:
            chatIdList.append(cid)
        return chatIdList
