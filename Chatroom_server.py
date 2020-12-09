import user_server
import ChatroomPool_server
# 個別聊天室內部使用者管理
# 0. 以隨機6碼由大寫英文、數字組合成之ID與指定名稱建立
# 1. 加入使用者
# 2. 使用者離開
# 3. 接收使用者發言
# 4. 聊天室內部訊息廣播
# 5. 向指定使用者傳遞特定訊息
# 6. 更動聊天室設定
# 8. 取得聊天室資訊


class Chatroom_server():
    # 0. 建立時以6碼大寫英文與數字組合之ID與2~10個字元長度聊天室名稱為參數建立
    # 建立時會帶入ChatroomPool作為事件傳遞參數
    def __init__(self, CID, name, managePool: ChatroomPool_server):
        self.CID = CID
        self.name = name
        self.managePool = managePool
        self.members = {}
        self.memberCount = 0

    def newMember(self, user):
        self.members[user.UID] = user
        self.memberCount += 1
        msg = user.name + " 加入了聊天室！"
        __innerBroadcast__(msg, [user.UID])
        __assignSend__(user, "成功加入聊天室。")
        # 1. 成員加入功能
        # 需帶入使用者連線類別作為參數傳入
        # 廣播訊息時將加入的使用者作為過濾參數，呼叫廣播功能，向本人以外的所有聊天室成員廣播「OOO 已加入聊天室」
        # 向加入的使用者傳遞「已成功加入聊天室」
        # 將該使用者加入使用者管理區

    def memberLeave(self, user):
        msg = user.name + " 已離開聊天室。"
        del self.members[user.UID]
        self.memberCount -= 1
        __innerBroadcast__(msg, [])
        __assignSend__(user, "您已離開聊天室。")
        if self.memberCount == 0:
            __close__()
        # if self.memberCount == 0:

        # 2. 成員離開功能
        # 該功能需將離開的使用者作為參數傳入
        # 廣播訊息時將離開的使用者作為過濾參數，呼叫廣播功能，向本人以外的所有聊天室成員廣播「OOO 已離開聊天室」
        # 向離開的使用者傳遞「已離開聊天室」
        # 將該使用者從使用者管理區移除
        # 如果聊天室沒有成員了，關閉聊天室

    def memberMessage(self, user, msg):
        message = user.name + ": " + msg
        __innerBroadcast__(message, [])
        # 3. 成員發言
        # 參數有發送者以及訊息

    def __innerBroadcast__(self, msg, excludingUser):
        for uid in self.members:
            if uid not in excludingUser:
                members[uid].send(msg)
        # 4. 聊天室內部訊息廣播，需帶入兩參數，第一個參數為傳遞的訊息，第二個參數為過濾使用者列表，預設為空字典
        # 向所有不再過濾列表中的使用者傳遞指定訊息

    def __assignSend__(self, receiver, msg):
        _receiver = self.members[receiver.UID]
        _receiver.send(msg)
        # 5. 向指定成員傳遞訊息，需帶入兩參數，第一個參數為指定的使用者，第二個參數為傳遞的訊息
        # 向指定使用者傳遞訊息

    def getChatroomInfo(self, getter):
        msg = self.CID + "\n" + self.name + "\n" + self.memberCount
        __assignSend__(getter, msg)
        # 8. 取得聊天室資訊
        # 回傳聊天室ID、名稱、人數

    def __close__(self):
        self.managePool.chatroomClose(self.CID)

        # 9. 關閉聊天室
        # 通知ChatroomPool該聊天室關閉
        # 回收該聊天室資源
