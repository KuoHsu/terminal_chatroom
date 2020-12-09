import ChatroomPool_server
import Chatroom_server
# 該類別為聊天室操作相關功能模組，包含建立、加入、離開、發言、設定聊天室


# 接收使用者傳遞訊息
# 建立聊天室
# 使用者加入指定聊天室
# 使用者離開指定聊天室
# 使用者在指定聊天室發言
# 使用者在指定聊天室進行設定操作
# 取得聊天室資訊列表

class ChatroomOperator():

    def __init__(self):
        super().__init__()
        self.chatroomPool = ChatroomPool_server()


# 1. 接收使用者傳遞訊息
# 該功能同時接收從使用者端傳來的聊天訊息、離開訊息、取得聊天室資訊
# 參數有發送訊息的使用者以及訊息
# 聊天訊息處理 - 向所有使用者廣播該訊息
# 離開訊息 - 呼叫使用者離開功能
# 取得聊天室資訊 -

    def createNewChatroom(self, creator):
        chatroom = chatroomPool.createNewChatroom()
        chatroom.newMember(creator)

    def userSendMessage(self, user, CID, msg):
        chatroom = self.chatroomPool.getChatroom(CID)
        chatroom.memberMessage(user, msg)
        return

    def joinChatroom(self, user, CID):
        chatroom = self.chatroomPool.getChatroom(CID)
        chatroom.newMember(user)

    def leaveChatroom(self, user, CID):
        chatroom = self.chatroomPool.getChatroom(CID)
        chatroom.memberLeave(user)
