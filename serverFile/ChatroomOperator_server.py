from serverFile.ChatroomPool_server import *
from serverFile.Chatroom_server import *
from serverFile.User_server import *
# 該類別為聊天室操作相關功能模組，包含建立、加入、離開、發言、設定聊天室


# 接收使用者傳遞訊息
# 建立聊天室
# 使用者加入指定聊天室
# 使用者離開指定聊天室
# 使用者在指定聊天室發言
# 取得聊天室資訊列表

class ChatroomOperator_server:

    def __init__(self):
        super().__init__()
        self.chatroomPool = ChatroomPool_server()

    def createNewChatroom(self, creator: User_server, name):
        chatroom = self.chatroomPool.createNewChatroom(name)
        chatroom.newMember(creator)
        cid = chatroom.getCID()

        return cid

    def userSendMessage(self, user: User_server, CID, msg):  # 聊天室成員發送訊息
        chatroom = self.chatroomPool.getChatroom(CID)
        chatroom.memberMessage(user, msg)
        return

    def joinChatroom(self, user: User_server, CID):
        chatroom = self.chatroomPool.getChatroom(CID)
        if chatroom is None:
            return False
        flag = chatroom.newMember(user)
        return flag

    def leaveChatroom(self, user: User_server, CID):
        chatroom = self.chatroomPool.getChatroom(CID)
        flag = chatroom.memberLeave(user)
        return flag

    def userDisconnect(self, user: User_server, CID):
        chatroom = self.chatroomPool.getChatroom(CID)
        if chatroom is None:
            return False
        flag = chatroom.memberDisconnect(user)
        return flag

    def getChatroomInfo(self, CID):
        chatroom = self.chatroomPool.getChatroom(CID)
        if chatroom is None:
            return "CID-error"
        msg = chatroom.getChatroomInfo()
        return msg

    def getChatroomList(self):
        return self.chatroomPool.getChatroomInfoList()

    def getUserJoinChatroomIDlist(self, user):
        cids = self.chatroomPool.getChatroomIDList()
        chatcid = []
        for cid in cids:
            chatroom = self.chatroomPool.getChatroom(cid)
            if chatroom != None and chatroom.isMember(user):
                chatcid.append(cid)
        return chatcid
