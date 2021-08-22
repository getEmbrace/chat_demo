
import time
import json
import hashlib
import datetime
import threading

import db1 as DB
import myHttp
import longSrc
import commHouse

useDb = DB.useDb
getDbuser = DB.getDbuser
mThread = longSrc.Mthread({
    "url": '/admin',
    "uid": 10000001,
    "thread": threading.currentThread()
})
commH = commHouse.CommHouse()

def index(params):
    with open('/root/vuePro_yujian/server/dist/index.html', 'r') as f:
        data = f.read()
        
    response = myHttp.response({
        'body': data,
        'headers': {
            'Content-Type': 'text/html'
        }
    })
    return response

def login(params):
    data = json.loads(params.get('bodys'))
    username = data.get('username')
    password = data.get('password')
    # 连接数据库
    status = useDb('user', "username = '{}'".format(username),
                   {"username": "", "password": ""},
                   None, {'username': username, 'password': password})
    if(status == 0):
        # 用户名或密码错误返回0
        data = {'status': 0}
    else:
        string = username + str(time.time())
        h1 = hashlib.md5()
        h1.update(string.encode(encoding='utf-8'))
        strmd5 = h1.hexdigest()
        useDb('user', "username = '{}'".format(data.get('username')),
              {'active': '1', 'cooike': strmd5,
                  'lastTime': str(datetime.datetime.today())},
              None, {'username': username, 'password': password}, 3)

        data = {'status': 1, 'data': {'cooike': strmd5}}

    response = myHttp.response({
        'body': str(data)
    })
    return response

def regist(params):
    data = json.loads(params.get('bodys'))
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    # 连接数据库
    userInfo = useDb('user', "username = '{}'".format(username), {"id": ""})
    if(userInfo):
        print(userInfo)
        # 用户存在
        data = {'status': 0}
    else:
        # 新建数据库用户
        sql_createUser = 'create user "{}"@"localhost" identified by "{}"'.format(
            username, password)
        res = useDb('', '', '', sql_createUser)
        if(res == 1):
            sql_setGrant = 'grant select, insert, delete, update on yujianDB.* to "{}"@"localhost"'.format(
                username)
            res = useDb('', '', '', sql_setGrant)
            sql = "flush privileges;"
            res = useDb('', '', '', sql)
            # 新建用户
            field = {
                'username': username,
                'password': password,
                'email': email,
                'active': '0',
                'friends': str([]),
                'firstTime': str(datetime.datetime.today()),
            }
            status = useDb('user', None, field, None,
                        {'username': username, 'password': password}, 1)
            if(status == 1):
                data = login(params)
                return data
            else:
                sql = 'drop user "{}"@"localhost";'.format(username)
                res = useDb('', '', '', sql)
                data = {'status': -1}
        else:
            data = {'status': 0}

    response = myHttp.response({
        'body': str(data)
    })
    return response

# 激活函数
def getFriends_pro(Alive):
    Alive.start()
    threadInfo = Alive.threadInfo
    cooike = threadInfo.get('uid')
    Dbuser = threadInfo.get('Dbuser')
    # 连接数据库
    userInfo = useDb('user', "cooike='{}'".format(cooike), 
                     {"id": "", "friends": ""}, None, Dbuser)
    mid = userInfo[0].get('id')
    friends = userInfo[0].get('friends')
    friendsId_arr = json.loads(friends)
    friendsArr = []
    for uid in friendsId_arr:
        userInfoById = useDb('user', "id='{}'".format(uid),
                             {"id": "", "username": "","picture": "", "active": ""}, 
                             None, Dbuser)
        # 获取该friend发送的未读消息
        MInfo = useDb('message', 
                "origin='{}' and dest='{}' and destKind='1' and (content not like 'tryComm/%' or Kind='0')".format(uid, mid),
                {"id": ""}, Dbuser=Dbuser)
        # 将有效通讯消息提取出来
        commInfo = useDb('message',
                    "(origin='{}' and dest='{}' and destKind='1' and Kind='1') and content like 'tryComm/%'".format(uid, mid),
                    {"id": "", "origin": ""}, Dbuser=Dbuser)
        if(userInfoById):
            if(MInfo):
                userInfoById[0]['messageCount'] = len(MInfo)
            else:
                userInfoById[0]['messageCount'] = 0 
            if(commInfo):
                userInfoById[0]['commInfo'] = commInfo
            friendsArr.append(userInfoById[0])  
    while(threadInfo.get('isAlive') == False):
        # 连接数据库
        userInfo1 = useDb('user', "cooike='{}'".format(cooike), 
                          {"friends": ""}, None, Dbuser)
        newFriends = userInfo1[0].get('friends')
        newfriendsId_arr = json.loads(newFriends)
        newfriendsArr = []
        for uid in newfriendsId_arr:
            userInfoById = useDb('user', "id='{}'".format(uid),
                                 {"id": "", "username": "","picture": "", "active": ""},
                                 None, Dbuser)
            # 获取该friend发送的未读消息
            MInfo = useDb('message', 
                    "origin='{}' and dest='{}' and destKind='1' and (content not like 'tryComm/%' or Kind='0' )".format(uid, mid),
                    {"id": ""}, Dbuser=Dbuser)
            # 将通讯消息提取出来
            commInfo = useDb('message', 
                    "(origin='{}' and dest='{}' and destKind='1' and Kind='1') and content like 'tryComm/%'".format(uid, mid),
                    {"id": "", "origin": ""}, Dbuser=Dbuser)
            if(userInfoById):
                if(MInfo):
                    userInfoById[0]['messageCount'] = len(MInfo)
                else:
                    userInfoById[0]['messageCount'] = 0 
                if(commInfo):
                    userInfoById[0]['commInfo'] = commInfo
                    useDb('message', 
                        "(origin='{}' and dest='{}' and destKind='1' and Kind='1') and content like 'tryComm/%'".format(uid, mid),
                        {"Kind": "0", "destKind":"0"}, Dbuser=Dbuser,type=3)
                newfriendsArr.append(userInfoById[0])
        if(friendsArr != newfriendsArr):
            threadInfo['backData'] = newfriendsArr
            Alive.next()
            break
        time.sleep(1)
# 挂起函数
def getFriends(params):
    data = json.loads(params.get('bodys'))
    cooike = data.get('cooike')
    # 连接数据库
    Dbuser = getDbuser("cooike='{}'".format(cooike))
    if(Dbuser):
        # 加入挂起列表: 阻塞到这通过激活函数后继续
        threadName = threading.currentThread().name
        print(threadName + ' waiting...')
        threadInfo = mThread.appendThread({
            "url": params.get('url'),
            "uid": cooike,
            "pro": getFriends_pro,
            "threadName": threadName,
            "Dbuser": Dbuser
        })
        print(threadName + ' alive')
        if(threadInfo.get('exitKind') == 1):
            # 关闭长链接 -2
            send_data = {'status': -2}
        elif(threadInfo.get('exitKind') == -1):
            # 连接数据库
            userInfo = useDb('user', "cooike='{}'".format(
                cooike), {"id": "", "friends": ""}, Dbuser=Dbuser)
            # print('uInfo', userInfo, Dbuser)
            friends = userInfo[0].get('friends')
            mid = userInfo[0].get('id')
            friendsId_arr = json.loads(friends)
            friendsArr = []
            for uid in friendsId_arr:
                userInfoById = useDb('user', "id='{}'".format(uid),
                                     {"id": "", "username": "",
                                      "picture": "", "active": ""}, Dbuser=Dbuser)
                if(userInfoById):
                    # 获取该friend发送的未读消息
                    MInfo = useDb('message', 
                        "origin='{}' and dest='{}' and destKind='1'".format(uid, mid),
                        {"id": "", }, Dbuser=Dbuser)
                    if(MInfo):
                        userInfoById[0]['messageCount'] = len(MInfo)      
                    else:
                        userInfoById[0]['messageCount'] = 0 
                        
                    friendsArr.append(userInfoById[0])
            send_data = {'status': 1, 'data': friendsArr}
        elif(threadInfo.get('exitKind') == 0):
            send_data = {'status': 1, 'data': threadInfo.get('backData')}
    else:
        send_data = {'status': 0}

    response = myHttp.response({
        'body': str(send_data)
    })

    return response

def findUser(params):
    data = json.loads(params.get('bodys'))
    cooike = data.get('cooike')
    username = data.get('username')
    # 连接数据库
    Dbuser = getDbuser("cooike='{}'".format(cooike))
    if(Dbuser):
        userInfo_id = useDb('user', "cooike='{}'".format(cooike), {"id": ""}, Dbuser=Dbuser)
        uid = userInfo_id[0].get('id')
        userInfo = useDb('user', "username like '%{}%'".format(username), {
            "id": "",
            "username": "",
            "picture": "",
            "active": ""
        }, Dbuser=Dbuser)
        if(userInfo):
            # 去除本身
            for item in userInfo:
                if(item.get('id') == uid):
                    userInfo.remove(item)
                    break
            if(len(userInfo) != 0):
                data = {'status': 1, 'data': userInfo}
            else:
                data = {'status': 0}
        else:
            data = {'status': 0}
    else:
        data = {'status': -1}
    response = myHttp.response({
        'body': str(data)
    })
    return response

def getUserInfo(params):
    data = json.loads(params.get('bodys'))
    uid = data.get('uid')
    # 连接数据库
    Dbuser = getDbuser("id='{}'".format(uid))
    if(Dbuser):    
        field = {"id": "","username": "",
                "picture": "","selectedPic": "",
                "signature_m": "","sex": "",
                "age": "","birthday": "",
                "cons": ""}
        userInfo = useDb('user', "id = '{}'".format(uid), field, Dbuser=Dbuser)
        data = {'status': 1, 'data': userInfo[0]}
    else:
        data = {'status': 0}

    response = myHttp.response({
        'body': str(data)
    })
    return response

def addFriend(params):
    data = json.loads(params.get('bodys'))
    uid = data.get('addFriendId')
    cooike = data.get('cooike')
    # 连接数据库
    Dbuser = getDbuser("cooike='{}'".format(cooike))
    if(Dbuser):
        userInfo = useDb('user', "cooike='{}'".format(cooike), 
                         {"id": "", "friends": ""}, Dbuser=Dbuser)
        friends = userInfo[0].get('friends')
        mid = userInfo[0].get('id')
        if(mid == uid):
            data = {'status': 0}
        else:
            friends_arr = json.loads(friends)
            friend_Dbuser = getDbuser("id='{}'".format(uid))
            if(friend_Dbuser):
                if(uid not in friends_arr):
                    friends_arr.append(uid)
                    useDb('user', "cooike = '{}'".format(cooike),
                                    {"friends": str(friends_arr)}, Dbuser=Dbuser, type=3)
                    data = {'status': 1,
                        'data': {'addFriendId': uid}}
                else:
                    # 重复添加
                    data = {'status': -1}
            else:
                # 好友不存在
                data = {'status': 0}
    else:
        # 用户不存在
        data = {'status': 0}

    response = myHttp.response({
        'body': str(data)
    })
    return response

def delFriend(params):
    data = json.loads(params.get('bodys'))
    uid = data.get('delFriendId')
    cooike = data.get('cooike')
    # 连接数据库
    Dbuser = getDbuser("cooike='{}'".format(cooike))
    if(Dbuser):
        userInfo = useDb('user', "cooike='{}'".format(cooike),
                       {"id": "", "friends": ""}, Dbuser = Dbuser)
        friends = userInfo[0].get('friends')
        friends_arr = json.loads(friends)
        friend_Dbuser = getDbuser("id='{}'".format(uid))
        if(friend_Dbuser):
            if(uid in friends_arr):
                friends_arr.remove(uid)
                useDb('user', "cooike = '{}'".format(cooike),
                      {"friends": str(friends_arr)}, Dbuser = Dbuser, type=3)
                data = {'status': 1,
                    'data': {'delFriendId': uid}}
            else:
                # 好友id不存在friends中
                data = {'status': -1}
        else:
            # 好友不存在
            data = {
                'status': 0
            }
    else:
        # 用户不存在
        data = {
            'status': 0
        }

    response = myHttp.response({
        'body': str(data)
    })
    return response

def setActive(params):
    data = json.loads(params.get('bodys'))
    cooike = data.get('cooike')
    active = data.get('active')
    # 连接数据库
    Dbuser = getDbuser("cooike='{}'".format(cooike))
    if(Dbuser):
        useDb('user', "cooike = '{}'".format(cooike), 
              {"active": str(active), 'lastTime': str(datetime.datetime.today())},
              Dbuser=Dbuser, type=3)
        data = {'status': 1}
    else:
        data = {'status': 0}

    response = myHttp.response({
        'body': str(data)
    })
    return response

def getMine(params):
    data = json.loads(params.get('bodys'))
    cooike = data.get('cooike')
    # 连接数据库
    Dbuser = getDbuser("cooike='{}'".format(cooike))
    if(Dbuser):
        userInfo = useDb('user', "cooike='{}'".format(cooike),
                        {"id": "", "username": "","picture": "", "active": ""},
                        Dbuser=Dbuser)
        send_data = {'status': 1, 'data': userInfo[0]}
    else:
        send_data = {'status': 0}
        
    response = myHttp.response({
        'body': str(send_data)
    })
    return response

def sendMessage(params):
    data = json.loads(params.get('bodys'))
    cooike = data.get('cooike')
    FriendId = data.get('FriendId')
    message = data.get('message')
    # 连接数据库
    Dbuser = getDbuser("cooike='{}'".format(cooike))
    if(Dbuser):
        userInfo = useDb('user', "cooike='{}'".format(cooike),
                        {"id": "", "active": ""}, Dbuser=Dbuser)
        uid = userInfo[0].get('id')
        isFriend = useDb('user', "id='{}'".format(FriendId),
                         {"id": "", "active": ""}, Dbuser=Dbuser)
        if(isFriend):
            friendActive = isFriend[0].get('active')
            if(friendActive == 1):
                # 用户为在线状态: 返回1 等待用户响应
                Kind = 1
                send_data = {'status': 1}
            elif(friendActive == 0):
                # 返回2 本次请求转为未读消息
                Kind = 0
                send_data = {'status': 2}
            elif(friendActive == 2):
                # 用户忙碌返回2 本次请求转为未读消息
                Kind = 0
                send_data = {'status': 3}
            # 插入消息表
            useDb('message', '', 
                  {"origin": str(uid), "dest": str(FriendId),
                    "content": "{}".format(message), 
                    "originKind": '0', "destKind": '1', "Kind": str(Kind)}, Dbuser=Dbuser, type=1)
        else:
            # 返回0 本次请求失败
            send_data = {'status': 0}
    else:
        send_data = {'status': 0}

    response = myHttp.response({
        'body': str(send_data)
    })
    return response

def getMessage_f_pro(Alive):
    # 设置激活条件
    threadInfo = Alive.threadInfo
    cooike = threadInfo.get('uid')
    friendId = threadInfo.get('friendId')
    Dbuser = threadInfo.get('Dbuser')
    isUser = useDb('user', "cooike='{}'".format(cooike),
                   {"id": "", "active": ""}, Dbuser=Dbuser)
    uid = isUser[0].get('id')
    Alive.start()
    while(threadInfo.get('isAlive') == False):
        allMessage = useDb('message', 
                           "(dest='{}' and origin='{}') and destKind='1'".format(uid, friendId),
                           {"id": "", "origin": "", "dest": "", "content": "",
                            "originKind": "", "destKind": ""},
                           Dbuser=Dbuser)
            
        if(allMessage):
            threadInfo['backMessage'] = allMessage
            Alive.next()

def getMessage_f(params):
    data = json.loads(params.get('bodys'))
    cooike = data.get('cooike')
    friendId = data.get('friendId')
    # 连接数据库
    Dbuser = getDbuser("cooike='{}'".format(cooike))
    if(Dbuser):
        # 加入挂起列表: 阻塞到这通过激活函数后继续
        threadName = threading.currentThread().name
        print(threadName + ' waiting...')
        threadInfo = mThread.appendThread({
            # 可在此向Pro函数传递参数
            "url": params.get('url'),
            "uid": cooike,
            "pro": getMessage_f_pro,
            "threadName": threadName,
            "friendId": friendId,
            "Dbuser": Dbuser
        })
        print(threadName + ' alive')

        isUser = useDb('user', "cooike='{}'".format(cooike),
                       {"id": "", "active": ""}, Dbuser=Dbuser)
        uid = isUser[0].get('id')
        # 首次退出
        if(threadInfo.get('exitKind') == -1):
            allMessage = useDb('message', 
                               "(dest='{}' and origin='{}') or (dest='{}' and origin='{}')"
                               .format(uid, friendId, friendId, uid),
                               {"id": "", "origin": "", "dest": "", "content": "",
                                "originKind": "", "destKind": ""},
                               Dbuser=Dbuser)
            if(allMessage):
                useDb('message', "(dest='{}' and origin='{}') and destKind='1'".format(uid, friendId),
                      {"destKind": "0"}, Dbuser=Dbuser, type=3)
                send_data = {'status': 1, 'data': allMessage}
            else:
                # 没有消息 0
                send_data = {'status': 0}
        # 激活退出
        elif(threadInfo.get('exitKind') == 0):
            send_data = {'status': 1, 'data': threadInfo.get('backMessage')}
            # 将消息状态设为0
            useDb('message', "(dest='{}' and origin='{}') and originKind='1'".format(friendId, uid),
                  {"originKind": "0"}, Dbuser=Dbuser, type=3)
            useDb('message', "(dest='{}' and origin='{}') and destKind='1'".format(uid, friendId),
                  {"destKind": "0"}, Dbuser=Dbuser, type=3)
        # 主动退出
        elif(threadInfo.get('exitKind') == 1):
            # 关闭长链接 -2
            send_data = {'status': -2}
    else:
        # 用户不存在 -1
        send_data = {'status': -1}
        
    response = myHttp.response({
        'body': str(send_data)
    })
    return response

def closeLongSrc(params):
    data = json.loads(params.get('bodys'))
    cooike = data.get('cooike')
    url = data.get('url')
    mThread.removeThread(cooike, url)
    # 保证移除完整
    mThread.end(cooike, url)
    response = myHttp.response({
        'body': str({
            'status': 1
        })
    })
    return response

def startLink_v_pro(Alive):
    # 设置激活条件
    threadInfo = Alive.threadInfo
    cooike = threadInfo.get('uid')
    friendId = threadInfo.get('friendId')
    Dbuser = threadInfo.get('Dbuser')
    isUser = useDb('user', "cooike='{}'".format(cooike),
                   {"id": "", "active": ""}, Dbuser=Dbuser)
    uid = isUser[0].get('id')
    Alive.start()
    while(threadInfo.get('isAlive') == False):
        accessMessage = useDb('message', 
                    "dest='{}' and origin='{}' and destKind='1' and content like 'accessComm/%'".format(uid, friendId),
                    {"id": "", "origin": ""},
                    Dbuser=Dbuser)
        refuseMessage = useDb('message', 
                    "dest='{}' and origin='{}' and destKind='1' and content like 'refuseComm/%'".format(uid, friendId),
                    {"id": "", "origin": ""},
                    Dbuser=Dbuser)
        
        if(accessMessage or refuseMessage):
            allMessage = [accessMessage, refuseMessage]
            threadInfo['backMessage'] = allMessage
            Alive.next() 

def startLink_v(params):
    data = json.loads(params.get('bodys'))
    cooike = data.get('cooike')
    friendId = data.get('friendId')
    Dbuser = getDbuser("cooike='{}'".format(cooike))
    if(Dbuser):
        # 加入挂起列表: 阻塞到这通过激活函数后继续
        threadName = threading.currentThread().name
        print(threadName + ' waiting...')
        threadInfo = mThread.appendThread({
            # 可在此向Pro函数传递参数
            "url": params.get('url'),
            "uid": cooike,
            "pro": startLink_v_pro,
            "threadName": threadName,
            "friendId": friendId,
            "Dbuser": Dbuser
        })
        print(threadName + ' alive')
        
        if(threadInfo.get('exitKind') == -1):
                send_data = {'status': 1}
        # 激活退出
        elif(threadInfo.get('exitKind') == 0):
            backMessage = threadInfo.get('backMessage')
            if(backMessage[0]):
                send_data = {'status': 3, 'data': backMessage[0][0]}
            elif(backMessage[1]):
                send_data = {'status': 2, 'data': backMessage[1][0]}
            # 将消息状态设为0
            useDb('message', "id='{}'".format(send_data.get('data').get('id')),
                    {"destKind": "0","Kind": "0"}, Dbuser=Dbuser, type=3)
            
        # 主动退出
        elif(threadInfo.get('exitKind') == 1):
            # 关闭长链接 -2
            send_data = {'status': -2}
    else:
        # 用户不存在 -1
        send_data = {'status': -1}
        
    response = myHttp.response({
        'body': str(send_data)
    })
    return response

def setMessageStatus(params):
    data = json.loads(params.get('bodys'))
    cooike = data.get('cooike')
    messageId = data.get('messageId')
    # 连接数据库
    Dbuser = getDbuser("cooike='{}'".format(cooike))
    if(Dbuser):
        useDb('message', "id='{}'".format(messageId),
              {"destKind": "0", "Kind": "0"}, Dbuser=Dbuser, type=3)
        send_data = {"status": 1}
    else:
        send_data = {"status": 0}
        
    response = myHttp.response({
        'body': str(send_data)
    })
    return response

def commHouse_v_pro(Alive):
    # 设置激活条件
    Alive.start()
    threadInfo = Alive.threadInfo
    cooike = threadInfo.get('uid')
    houseNum = threadInfo.get('houseNum')
    Dbuser = threadInfo.get('Dbuser')
    isUser = useDb('user', "cooike='{}'".format(cooike),
                   {"id": "", "active": ""}, Dbuser=Dbuser)
    uid = isUser[0].get('id')
    
    while(threadInfo.get('isAlive') == False):
        # 对方退出
        if(commH.getHouseByNum(houseNum) == 0):
            message = 'close'
            threadInfo['backMessage'] = message
            Alive.next()
        if(commH.getMesssgeLength(houseNum, uid) > 0): 
            print('\n...', commH.getMesssgeLength(houseNum, uid), '...\n')  
            message = b'' 
            messageL = commH.getMessage(houseNum, uid, 10)
            if(messageL):
                for i in messageL:
                    # 主动退出
                    if(i == b'close'):
                        print(uid, 'close')
                        message = 'close'
                        commH.delHouse(houseNum)
                        break
                    message = message + i
                threadInfo['backMessage'] = message
                Alive.next()
        
def commHouse_v(params):
    data = json.loads(params.get('bodys'))
    cooike = data.get('cooike')
    friendId = data.get('friendId')
    houseNum = data.get('houseNum')
    Dbuser = getDbuser("cooike='{}'".format(cooike))
    content_type = 'application/json'
    if(Dbuser):
        User = useDb('user', "cooike='{}'".format(cooike),
                        {"id": "", "active": ""}, Dbuser=Dbuser)
        mid = User[0].get('id')
        # 加入挂起列表: 阻塞到这通过激活函数后继续
        threadName = threading.currentThread().name
        print(threadName + ' waiting...')
        threadInfo = mThread.appendThread({
            # 可在此向Pro函数传递参数
            "url": params.get('url'),
            "uid": cooike,
            "pro": commHouse_v_pro,
            "threadName": threadName,
            "friendId": friendId,
            "Dbuser": Dbuser,
            "houseNum": houseNum
        })
        print(threadName + ' alive')
        if(threadInfo.get('exitKind') == -1):
            # 判断对方是否已生成房间号
            houseInfo = commH.appendMemberByC(friendId, mid)
            send_data = str({'status': houseInfo[0], 'data': {'houseNum': houseInfo[1]}})
        elif(threadInfo.get('exitKind') == 0):
            message = threadInfo.get('backMessage')
            if(type(message).__name__ == 'bytes'):
                content_type = 'video/webm'
                send_data = message
            elif(type(message).__name__ == 'str'):
                send_data = str({'status': 3, 'data': message})                
        elif(threadInfo.get('exitKind') == 1):
            send_data = str({'status': -2})
    else:
       send_data = str({'status': -1})

    response = myHttp.response({
        'headers': {'Content-Type': content_type},
        'body': send_data
    })
    return response

def setHouseMessage(params):
    try:
        data = params.get('body')
    except:
        print(11, 'err')
        send_data = {'status': 1}
        response = myHttp.response({
            'body': str(send_data)
        })
        return response
    cooike = str(data.get('"cooike"'), encoding='utf-8')
    friendId = str(data.get('"friendId"'), encoding='utf-8')
    houseNum = str(data.get('"houseNum"'), encoding='utf-8')
    message = data.get('"message"')
    Dbuser = getDbuser("cooike='{}'".format(cooike))
    # print(cooike, friendId, houseNum)
    print(message[0: 30])
    if(Dbuser):
        if(houseNum != 0):
            while(commH.getMesssgeLength(houseNum, friendId) > 30):
                pass
            res = commH.setMessage(houseNum, friendId, message)
            send_data = {'status': res}
        else:
           send_data = {'status': -1}
    else:
        send_data = {'status': -1}
       
    response = myHttp.response({
        'body': str(send_data)
    })
    return response

def webSockte(params):
    print(params)


routers = {
    '/': index,
    '/home': index,
    '/login': login,
    '/regist': regist,
    '/getFriends': getFriends,
    '/findUser': findUser,
    '/getUserInfo': getUserInfo,
    '/addFriend': addFriend,
    '/delFriend': delFriend,
    '/setActive': setActive,
    '/getMine': getMine,
    '/sendMessage': sendMessage,
    '/getMessage_f': getMessage_f,
    '/closeLongSrc': closeLongSrc,
    '/startLink_v': startLink_v,
    '/setMessageStatus': setMessageStatus,
    '/commHouse': commHouse_v,
    '/setHouseMessage': setHouseMessage,
    '/webSockte': webSockte,
}
