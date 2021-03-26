import socket
import threading
from serverFile.UserPool_server import *
from serverFile.User_server import *
from serverFile.ChatroomOperator_server import *


class MainProcess_server:
    def __init__(self):
        self.userPool = UserPool_server()
        self.chatroomOperator = ChatroomOperator_server()

    def mainProcess(self, socket, addr):

        user = self.registe(socket, addr)
        run = True

        print("%s run on thread %s" %
              (user.name, threading.get_ident()))
        while run:
            try:
                msg = user.getMessage()
                msgType = msg["type"]
                msgAction = msg["action"]
                msgContent = msg["content"]
                if msgType == "operate":
                    run = self.hallOperating(user, msgAction, msgContent)
                elif msgType == "chatroom":
                    self.chatroomOperating(user, msgAction, msgContent)
                    # send msg, leave chatroom
            except:
                print("[連線]%s(%s) 意外斷線了。" % (user.getName(), user.getUID()))
                cids = self.chatroomOperator.getUserJoinChatroomIDlist(
                    user)
                for cid in cids:
                    self.chatroomOperating(user, "disconnect", cid)
                self.userPool.removeUser(user.getUID())
                run = False
                for thread in threading.enumerate():
                    print("thread:%s id:%d" % (thread.name, thread.ident))

    def registe(self, socket, addr):
        userName = socket.recv(1024).decode("UTF-8")
        newUser = self.userPool.newUser(socket, userName)
        uid = newUser.getUID()
        newUser.send("init", "registe", uid)
        address = "%s:%d" % (addr[0], addr[1])
        print("[連線] %s 已連線。連線來源: %s | UID: %s" % (userName, address, uid))
        return newUser

    def hallOperating(self, user, action, content):
        flag = True
        uid = user.getUID()
        uname = user.getName()

        if action == "listChatrooms":
            user.send("operate", "listChatrooms",
                      self.chatroomOperator.getChatroomList())
        elif action == "joinChatroom":
            cid = content
            joinFlag = self.chatroomOperator.joinChatroom(user, cid)
            if joinFlag:
                user.send("operate", "joinChatroom", "success")

                print("[聊天室 - %s] %s(%s) 加入聊天室。" % (cid, uname, uid))
            else:
                user.send("operate", "joinChatroom", "fail")
        elif action == "createNewChatroom":
            name = content
            cid = self.chatroomOperator.createNewChatroom(user, name)
            user.send("operate", "createNewChatroom", cid)
            print("[聊天室 - %s] 聊天室建立，聊天室名稱 %s，建立者 %s(%s)" %
                  (cid, name,  uname, uid))

        elif action == "disconnect":
            user.send("operate", "disconnect", "ok")
            user.disconnect()
            self.userPool.removeUser(user.getUID())
            print("[連線] %s(%s) 離線了" % (uname, uid))
            flag = False
        return flag

    def chatroomOperating(self, user, action, content):
        uid = user.getUID()
        uname = user.getName()
        if action == "msg":
            cid = content["CID"]
            msg = content["msg"]
            self.chatroomOperator.userSendMessage(user, cid, msg)
            print("[聊天室 - %s] %s(%s): %s" % (cid, uname, uid, msg))

        elif action == "getInfo":
            cid = content
            msg = self.chatroomOperator.getChatroomInfo(cid)
            user.send("chatroom", "getInfo", msg)
        elif action == "leave":
            cid = content
            flag = self.chatroomOperator.leaveChatroom(user, cid)
            if flag:
                user.send("chatroom", "leave", "success")
                print("[聊天室 - %s] %s(%s) 離開聊天室。" % (cid, uname, uid))
            else:
                user.send("chatroom", "leave", "fail")
        elif action == "disconnect":
            cid = content
            flag = self.chatroomOperator.userDisconnect(user, cid)
            if flag:
                print("[聊天室 - %s] %s(%s) 斷線了。" % (cid, uname, uid))
