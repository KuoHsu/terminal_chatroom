import ChatroomPool_server
import Chatroom_server
import User_server
# 該類別為聊天室操作相關功能模組，包含建立、加入、離開、發言、設定聊天室


# 接收使用者傳遞訊息
# 建立聊天室
# 使用者加入指定聊天室
# 使用者離開指定聊天室
# 使用者在指定聊天室發言
# 取得聊天室資訊列表

class ChatroomOperator():

    def __init__(self):
        super().__init__()
        self.chatroomPool = ChatroomPool_server()

    def createNewChatroom(self, creator: User_server):
        chatroom = chatroomPool.createNewChatroom()
        flag = chatroom.newMember(creator)
        return flag

    def userSendMessage(self, user: User_server, CID, msg):
        chatroom = self.chatroomPool.getChatroom(CID)
        chatroom.memberMessage(user, msg)
        return

    def joinChatroom(self, user: User_server, CID):
        chatroom = self.chatroomPool.getChatroom(CID)
        flag = chatroom.newMember(user)
        return flag

    def leaveChatroom(self, user: User_server, CID):
        chatroom = self.chatroomPool.getChatroom(CID)
        flag = chatroom.memberLeave(user)
        return flag

    def getChatroomInfo(self, CID):
        chatroom = self.chatroomPool.getChatroom(CID)
        msg = chatroom.getChatroomInfo()
        return msg

    def getChatroomList(self):
        return chatroomPool.getChatroomList()
