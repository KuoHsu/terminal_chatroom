import socket
import threading
import time

target_host = '127.0.0.1'
target_port = 8888

# create a IPV4, TCP connection socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_host, target_port))

balance = 10000
stock = {"沙魚": 10,
         "軟絲": 10,
         "花蟹": 10,
         "花蟹(小的)": 10,
         "花蟹(再小一點)": 10,
         "大沙母": 10,
         "海瓜子": 10,
         "奶油貝": 10,
         "生蠔": 10,
         "木瓜螺": 10,
         "小花龍": 10,
         "水姑娘": 10,
         "象蚌": 10}
productList = ["沙魚", "軟絲", "花蟹", "花蟹(小的)", "花蟹(再小一點)",
               "大沙母", "海瓜子", "奶油貝", "生蠔", "木瓜螺", "小花龍", "水姑娘", "象蚌"]


def buyProduct(client):
    msg = {}
    exitFlag = False
    flagForSelectProduct = True
    global balance
    while flagForSelectProduct:
        # 選擇漁貨
        selectedIndex = input(
            "請選擇要購買的漁貨\n\r(1)沙魚\n\r(2)軟絲\n\r(3)花蟹\n\r(4)花蟹(小的)\n\r(5)花蟹(再小一點)\n\r(6)大沙母\n\r(7)海瓜子\n\r(8)奶油貝\n\r(9)生蠔\n\r(10)木瓜螺\n\r(11)小花龍\n\r(12)水姑娘\n\r(13)象蚌\n\r(0)離開\n\r")
        index = int(selectedIndex)
        if index > 0 and index <= 13:
            msg["product"] = productList[index-1]
            msg["optionCode"] = 1
            flagForSelectProduct = False
            flagForAmount = True
            while flagForAmount:
                _amount = input("請輸入欲購買的數量(1~20)：")
                amount = int(_amount)
                if (amount > 0 and amount <= 20):
                    msg["amount"] = amount
                    msg["balance"] = balance
                    flagForAmount = False
                    flagForSelectProduct = False
                else:
                    print("請輸入有效數量(1~20)")
        elif index == 0:
            exitFlag = True
            flagForSelectProduct = False
        else:
            print("請輸入有效數字(0~13)")
    # socket send msg to server
    if exitFlag == False:
        emsg = str(msg).encode('UTF-8')
        client.send(emsg)


def sellProduct(client):
    global balance
    msg = {}
    flagForSelectProduct = True
    exitFlag = False
    while flagForSelectProduct:
        # 選擇漁貨
        selectedIndex = input(
            "請選擇要販賣的漁貨\n\r(1)沙魚\n\r(2)軟絲\n\r(3)花蟹\n\r(4)花蟹(小的)\n\r(5)花蟹(再小一點)\n\r(6)大沙母\n\r(7)海瓜子\n\r(8)奶油貝\n\r(9)生蠔\n\r(10)木瓜螺\n\r(11)小花龍\n\r(12)水姑娘\n\r(13)象蚌\n\r(0)離開\n\r")
        index = int(selectedIndex)
        if index > 0 and index <= 13:
            pName = productList[index - 1]
            stockAmount = stock[pName]

            if stockAmount > 0:  # 指定漁貨有存貨
                flagForSelectProduct = False
                flagForAmount = True
                msg["product"] = pName

                while flagForAmount:
                    _amount = input("請輸入欲販賣的數量(1~%d)：" % stockAmount)
                    amount = int(_amount)
                    if (amount > 0 & amount <= stockAmount):
                        msg["amount"] = amount
                        msg["optionCode"] = 2
                        stock[pName] -= amount
                        flagForAmount = False
                        flagForSelectProduct = False
                    else:
                        print("請輸入有效數量(1~%d)" % stockAmount)
            else:
                print("選擇的漁貨沒存貨了，換一個吧")

        elif index == 0:
            flagForSelectProduct = False
            exitFlag = True
        else:
            print("請輸入有效數字(0~13)")

    if exitFlag == False:
        emsg = str(msg).encode('UTF-8')
        client.send(emsg)


def getProductPrice(client):
    msg = {"optionCode": 3}
    client.send(str(msg).encode("UTF-8"))
   # responseMsg = client.recv(4096).decode("UTF-8")
   # responseDict = eval(responseMsg)
    # print(responseDict)


def printStockInfo():
    for k in stock:
        print("%s 尚有 %d 隻" % (k, stock[k]))


def printBlance():
    print("餘額尚有 %d 元" % balance)


def receiveMsg(socket):
    global balance
    flag = True
    while flag:
        responseMsg = client.recv(4096).decode("UTF-8")
        responseDict = eval(responseMsg)
        code = responseDict["statusCode"]
        if (code == 1):
            cost = responseDict["cost"]
            pName = responseDict["product"]
            amount = responseDict["amount"]
            stock[pName] += amount
            balance -= cost
            print("%s\n\r" % responseDict["message"])
        elif (code == 2):
            revenue = responseDict["revenue"]
            pName = responseDict["product"]
            balance += revenue
            print("%s\n\r" % responseDict["message"])
        elif (code == 3):
            plist = responseDict["list"]
            for k in plist:
                _p = plist.get(k)
                _a = _p.get("amount")
                _pr = _p.get("price")
                print("%s \n\r單價：%.2f \n\r" % (k, _pr))
        elif (code == -1):
            print("%s\n\r" %
                  responseDict["errorMessage"])
        elif (code == 0):
            print(responseDict["msg"])
        elif (code == 999):
            flag = False


print("連線成功")
print("歡迎來到 東太平洋漁場時價分析師兼操盤手暨洋流講師海龍王彼得 所經營的新鮮魚貨市場！")

registe = False
while not registe:
    user_name = input("請輸入你的使用者名稱：")
    client.send(user_name.encode("UTF-8"))
    response = client.recv(1024).decode("UTF-8")
    if response != "exist":
        registe = True
    else:
        print("有這個人囉\n\r")


print(user_name + " 歡迎進入市場，以下為你的存貨與餘額資訊：")
printStockInfo()
printBlance()

threadFlag = True
broadcastHandle = threading.Thread(target=receiveMsg, args=(client,))
broadcastHandle.start()

while True:
    time.sleep(0.5)
    print("------------------------------------------------------------")
    selection = int(input(
        "選擇操作選項：(1)買入新鮮漁貨 (2)賣出現有漁貨 (3)查看市場時價 (4)查看自身現存漁貨與餘額 (0)退出市場\n\r"))

    if selection == 1:
        buyProduct(client)
    elif selection == 2:
        sellProduct(client)
    elif selection == 3:
        getProductPrice(client)
    elif selection == 4:
        printStockInfo()
        printBlance()
    elif selection == 0:
        client.send(str({"optionCode": 0}).encode("UTF-8"))
        broadcastHandle.join()
        exit()
    # client.send(selection.encode("UTF-8"))

    #serverMsg = client.recv(4096).decode("UTF-8")

    # print(serverMsg)
