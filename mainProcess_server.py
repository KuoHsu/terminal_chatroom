import socket
import UserPool_server
import User_server
import ChatroomOperator_server


userPool = UserPool_server()
chatroomOperator = ChatroomOperator_server()


def mainProcess(socket, addr):
    user = registe(socket)
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


def registe(socket):
    userName = socket.recv(1024).decode("UTF-8")
    newUser = userPool.newUser(socket, userName)
    newUser.send("init", "registe", "ok")
    return newUser


def operate(user, action, content):
    flag = True
    if action == "listChatrooms":
        user.send("operate", "listChatrooms",
                  chatroomOperator.getChatroomList())
    elif action == "createNewChatroom":
        flag = chatroomOperator.createNewChatroom(user)
        if flag:
            user.send("chatroom", "join", "success")
        else:
            user.send("chatroom", "join", "fail")
    elif action == "disconnect":
        user.send("operate", "leave", True)
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
