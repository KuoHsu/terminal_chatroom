import socket
import threading
from clientFile.User_client import *


chatroomID = ""


def mainProcess(socket):
    user = registe(socket)
    run = True
    t = 1
    while run:
        if t == 1:
            operate(user)
        elif t == 2:
            chatroom(user, chatroomID)
        elif t == 3:
            run = False
            user.close()


def operate(user):
    f = 1
    while f == 1:
        selection = input("請選擇操作項目 (1).查看聊天室列表 (2).加入聊天室 (3).創建聊天室 (0).離開\n")
        if selection == "1":
            user.send("operate", "listChatrooms", "")
        elif selection == "2":
            cid = input("請輸入聊天室ID: ")
            user.send("operate", "joinChatroom", cid)
            msg = user.getMsg()
            if (msg["content"] == "success"):
                chatroomID = cid
                f = 2
            else:
                print("Join fail")
        elif selection == "3":
            name = input("請輸入聊天室名: ")
            user.send("operate", "createNewChatroom", name)
            cid = user.getMsg("content")
            chatroomID = cid
            f = 2
        elif selection == "0":
            user.send("operate", "disconnect", "")
            msg = user.getMsg()
            if msg["content"] == "ok":
                f = 3
        else:
            print("請輸入 1, 2, 3或0！\n")
    return f


def chatroom(user, cid):
    f = 2
    print("聊天室操作： 輸入 -info 取得聊天室資訊；輸入 -exit 離開聊天室")
    chatroomMsgThread = threading.Thread(
        target=listenChatroomMsg, args=(user,))
    chatroomMsgThread.start()
    while f == 2:
        inputText = input(">> ")
        if inputText == "-info":
            user.send("chatroom", "getInfo", cid)
        elif inputText == "-exit":
            user.send("chatroom", "leave", cid)
            f = 1
        else:
            content = {"cid": cid, "msg": inputText}
            user.send("chatroom", "msg", content)
    chatroomMsgThread.join()
    return f


def listenChatroomMsg(user):
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
            flag = False


def registe(socket):
    name = input("Enter the name: ")
    init_msg = name
    enmsg = str(init_msg).encode("UTF-8")
    socket.send(enmsg)
    recmsg = socket.recv(2048).decode("UTF-8")
    msg = eval(recmsg)
    uid = ""

    if msg["type"] == "init":
        uid = msg["content"]

    user = User_client(socket, name, uid)
    return user
