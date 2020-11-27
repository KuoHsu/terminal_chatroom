import socket
import threading

# 購買產品


def clientBuyProduct(userName, pName, amount, balance):
    msg = {"statusCode": 0}
    if (pName in product):
        # 取得產品資訊(售價、剩餘數量)
        _product = product[pName]
        if(amount > 0 and _product["amount"] >= amount):
            oldPrice = _product["price"]
            cost = amount * oldPrice
            if (cost > balance):
                # 總售價大於使用者餘額
                msg["statusCode"] = -1
                msg["errorMsg"] = "你確定你有足夠的錢嗎？這要花你 %.2f 元喔" % cost
            else:
                newAmount = _product["amount"] - amount
                newPrice = round(oldPrice + (oldPrice * 0.01)
                                 ** (amount / 20), 2)
                _product["price"] = newPrice
                _product["amount"] = newAmount

                # ====回傳訊息設定
                msg["statusCode"] = 1
                msg["message"] = "你只要相信海，海就會幫助你，你用 %.2f 元買了 %d 隻 %s" % (
                    cost, amount, pName)
                msg["product"] = pName
                msg["amount"] = amount
                msg["cost"] = cost
                # ====

                print("%s 以時價 %.2f 買了 %d 隻 %s" %
                      (userName, oldPrice, amount, pName))
                print("%s 時價變動為 %.2f，剩餘數量為 %d" % (pName, newPrice, newAmount))
                broadcast("[!] %s 漲價了！" % pName)
        else:
            msg["statusCode"] = -1
            msg["errorMessage"] = "庫存不夠欸，你要不要買別的"
            print(amount)
    else:
        msg["statusCode"] = -1
        msg["errorMessage"] = "海龍王沒賣這種海鮮"
    return msg

# 使用者販售產品


def connectionPoolellProduct(userName, pName, amount):

    msg = {"statusCode": 0}
    if (pName in product):
        # 取得產品資訊(售價、剩餘數量)
        _product = product[pName]
        if(amount > 0):
            oldPrice = _product["price"]
            newAmount = _product["amount"] + amount

            newPrice = round(oldPrice - (oldPrice * 0.009901)
                             ** (amount / 20), 2)

            _product["price"] = newPrice
            _product["amount"] = newAmount
            msg["statusCode"] = 2
            msg["message"] = "你以總價 %.2f 的價錢將 %d 隻 %s賣給了海龍王，海龍王會感謝你的" % (
                oldPrice * amount, amount, pName)
            msg["product"] = pName
            msg["amount"] = amount
            msg["revenue"] = oldPrice * amount
            print("%s 以時價 %.2f 賣了 %d 隻 %s" %
                  (userName, oldPrice, amount, pName))
            print("%s 時價變動為 %.2f，剩餘數量為 %d" % (pName, newPrice, newAmount))
            broadcast("[!] %s 降價了！" % pName)
        else:
            msg["statusCode"] = -1
            msg["errorMessage"] = "你的貨呢"
    else:
        msg["statusCode"] = -1
        msg["errorMessage"] = "海龍王不收購這種東西"
    return msg


def lookProductList():
    msg = {"statusCode": 3}
    msg["list"] = product
    return msg

# 對全部使用者廣播


def broadcast(msg):
    emsg = {"statusCode": 0, "msg": msg}
    for user_name in connectionPool:
        client = connectionPool.get(user_name)
        client.send(str(emsg).encode("UTF-8"))


# 使用者主程序函式
def connection_thread(connection_Socket, addr):
    user_name = connection_Socket.recv(1024).decode("UTF-8")
    while user_name in connectionPool:
        connection_Socket.send("exist".encode("UTF-8"))
        user_name = connection_Socket.recv(1024).decode("UTF-8")

    connection_Socket.send("enter ok".encode("UTF-8"))
    connectionPool[user_name] = connection_Socket
    address = "%s:%d" % (addr[0], addr[1])
    print("[!] 來自 %s 的 %s 進入市場了" % (address, user_name))

    broadcast("[!] 有新的使用者進入市場了！")

    run = True

    while run:

        try:
            dmsg = connection_Socket.recv(1024).decode("UTF-8")
            msg = eval(dmsg)

            responseMsg = {}

            if msg["optionCode"] == 1:
                pName = msg["product"]
                amount = int(msg["amount"])
                balance = int(msg["balance"])
                responseMsg = clientBuyProduct(
                    user_name, pName, amount, balance)
                # ...
            elif msg["optionCode"] == 2:
                pName = msg["product"]
                amount = int(msg["amount"])
                responseMsg = connectionPoolellProduct(
                    user_name, pName, amount)
                # ...
            elif msg["optionCode"] == 3:
                responseMsg = lookProductList()
                # ...
            elif msg["optionCode"] == 0:
                responseMsg = {"statusCode": 999}

            response = str(responseMsg).encode('UTF-8')
            connection_Socket.send(response)

            if msg["optionCode"] == 0:
                run = False
                del connectionPool[user_name]
                connection_Socket.close()
                print("[!] %s 離線了" % user_name)
                broadcast("[!] 有使用者離開市場了！")
        # 'connection_Socket.close()
        except:
            print("[!] %s 意外斷線了" % user_name)
            del connectionPool[user_name]
            broadcast("[!] 有使用者離開市場了！")
            run = False


# --------------------------------------------------
# server端的資料
product = {"沙魚": {"amount": 1000, "price": 450},
           "軟絲": {"amount": 1000, "price": 850},
           "花蟹": {"amount": 1000, "price": 750},
           "花蟹(小的)": {"amount": 1000, "price": 450},
           "花蟹(再小一點)": {"amount": 1000, "price": 350},
           "大沙母": {"amount": 1000, "price": 850},
           "海瓜子": {"amount": 1000, "price": 180},
           "奶油貝": {"amount": 1000, "price": 250},
           "生蠔": {"amount": 1000, "price": 180},
           "木瓜螺": {"amount": 1000, "price": 350},
           "小花龍": {"amount": 1000, "price": 1250},
           "水姑娘": {"amount": 1000, "price": 1680},
           "象蚌": {"amount": 1000, "price": 650}}

# ----------------------------------------------
# 連線使用者的字典，以使用者名稱為key，用來管理使用者連線執行序
connectionPool = {}

# ---------------------------------------------
# server setting
host = "127.0.0.1"
port = 8888

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen(1)
print("海龍王市場開市")

while True:
    connection_Socket, addr = server.accept()

    connectThread = threading.Thread(
        target=connection_thread, args=(connection_Socket, addr,))
    connectThread.start()
