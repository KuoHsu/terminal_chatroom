import socket
from serverFile.UserPool_server import *
from serverFile.User_server import *
from serverFile.ChatroomOperator_server import *


userPool = UserPool_server()
chatroomOperator = ChatroomOperator_server()


def mainProcess(socket, addr):

    user = registe(socket, addr)
    run = True
    while run:
        msg = user.getMessage()
        msgType = msg["type"]
        msgAction = msg["action"]
        msgContent = msg["content"]
        if msgType == "operate":
            run = operate(user, msgAction, msgContent)
        elif msgType == "chatroom":
            chatroom(user, msgAction, msgContent)
            # send msg, leave chatroom


def registe(socket, addr):
    userName = socket.recv(1024).decode("UTF-8")
    newUser = userPool.newUser(socket, userName)
    uid = newUser.getUID()
    newUser.send("init", "registe", uid)
    address = "%s:%d" % (addr[0], addr[1])
    print("連線來源: %s UID: %s 使用者名稱: %s 已連線" % (address, uid, userName))
    return newUser


def operate(user, action, content):
    flag = True
    if action == "listChatrooms":

        user.send("operate", "listChatrooms",
                  chatroomOperator.getChatroomList())
    elif action == "join":
        cid = content
        flag = chatroomOperator.joinChatroom(user, cid)
        if flag:
            user.send("operate", "joinChatroom", "success")
        else:
            user.send("operate", "joinChatroom", "fail")
    elif action == "createNewChatroom":
        name = content
        cid = chatroomOperator.createNewChatroom(user, name)
        user.send("operate", "createNewChatroom", cid)
    elif action == "disconnect":
        user.send("operate", "disconnect", "ok")
        user.disconnect()
        userPool.removeUser(user.getUID())
        flag = False
    return flag


def chatroom(user, action, content):
    if action == "msg":
        cid = content["CID"]
        msg = content["msg"]
        chatroomOperator.userSendMessage(user, cid, msg)

    elif action == "getInfo":
        cid = content
        msg = chatroomOperator.getChatroomInfo(cid)
        user.send("chatroom", "getInfo", msg)
    elif action == "leave":
        cid = content
        flag = chatroomOperator.leaveChatroom(user, cid)
        if flag:
            user.send("chatroom", "leave", "success")
        else:
            user.send("chatroom", "leave", "fail")
