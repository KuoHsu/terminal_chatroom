import socket
import threading
from clientFile.User_client import *


class MainProcess_Client:
    def __init__(self):
        self.chatroomID = ""

    def mainProcess(self, socket):

        user = self.registe(socket)
        run = True
        t = 1
        while run:
            try:
                if t == 1:
                    t = self.hallOperating(user)
                elif t == 2:
                    t = self.chatroomOperating(user, self.chatroomID)
                    self.chatroomID = ""
                elif t == 3:
                    run = False
                    user.close()
            except:
                print("無法連上伺服器！")
                exit()

    def hallOperating(self, user):
        f = 1
        while f == 1:
            selection = input(
                "請選擇操作項目 (1).查看聊天室列表 (2).加入聊天室 (3).創建聊天室 (0).離開\n")
            if selection == "1":
                user.send("operate", "listChatrooms", "")
                msg = user.getMsg()
                print(msg["content"])
            elif selection == "2":
                cid = input("請輸入聊天室ID: ")
                user.send("operate", "joinChatroom", cid)
                msg = user.getMsg()
                if (msg["content"] == "success"):
                    self.chatroomID = cid
                    f = 2
                else:
                    print("加入失敗！檢查聊天室代碼是否打錯")
            elif selection == "3":
                name = input("請輸入聊天室名: ")
                user.send("operate", "createNewChatroom", name)
                msg = user.getMsg()
                self.chatroomID = msg["content"]
                f = 2
            elif selection == "0":
                user.send("operate", "disconnect", "")
                msg = user.getMsg()
                if msg["content"] == "ok":
                    f = 3
            else:
                print("請輸入 1, 2, 3或0！\n")
        return f

    def chatroomOperating(self, user, cid):
        f = 2
        chatroomMsgThread = threading.Thread(
            target=self.listenChatroomMsg, args=(user,))
        chatroomMsgThread.start()
        print("您已加入聊天室！")
        print("聊天室操作： 輸入 -info 取得聊天室資訊；輸入 -exit 離開聊天室")

        while f == 2:
            inputText = input("")
            if inputText == "-info":
                user.send("chatroom", "getInfo", cid)
            elif inputText == "-exit":
                user.send("chatroom", "leave", cid)
                f = 1
            elif inputText == "":
                f = 2
            else:
                content = {"CID": cid, "msg": inputText}
                user.send("chatroom", "msg", content)
        chatroomMsgThread.join()
        return f

    def listenChatroomMsg(self, user):
        flag = True
        while flag:
            msg = user.getMsg()
            action = msg["action"]
            msg = msg["content"]
            if action == "msg":
                print(msg)
            elif action == "getInfo":
                print(msg)
            elif action == "leave" and msg == "success":
                print("您已離開聊天室！\n")
                flag = False

    def registe(self, socket):
        name = input("請輸入使用者名稱: ")
        init_msg = name
        enmsg = str(init_msg).encode("UTF-8")
        socket.send(enmsg)
        recmsg = socket.recv(2048).decode("UTF-8")
        msg = eval(recmsg)
        uid = ""

        if msg["type"] == "init":
            uid = msg["content"]
            print("%s 歡迎登入！" % name)

        user = User_client(socket, name, uid)
        return user
