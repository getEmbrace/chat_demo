# -*- coding:utf-8 -*-
import json
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver
import asyncio

import db1 as DB

useDb = DB.useDb
getDbuser = DB.getDbuser
waiters_g = []
class ChatHandler(tornado.websocket.WebSocketHandler):
    # 用户存储当前聊天室用户
    # waiters = set()
    
    def check_origin(self, origin):
        return True

    def open(self):
        """
        客户端连接成功时，自动执行
        :return: 
        """
        # 向waiters加入
        waiters_g.append({'self': self, 'selfId': '' ,'friends': []})
        # print(waiters_g)

    def on_message(self, message):
        """
        客户端发送消息时，自动执行
        :param message: 
        :return: 
        """
        # 对链接进行验证
        if(type(message).__name__ == 'str'):
            msg = json.loads(message)
            cooike = msg.get('cooike')
            friendId = msg.get('friendId')
            Dbuser = getDbuser("cooike='{}'".format(cooike))
            if(Dbuser):
                User = useDb('user', "cooike='{}'".format(cooike),
                        {"id": "", "active": ""}, Dbuser=Dbuser)
                mid = User[0].get('id')
                # 填充信息
                for item in waiters_g:
                    if(item.get('self') == self):
                        item['selfId'] = mid
                        item.get('friends').append(friendId) 
                        print('userId:', mid,'--', friendId, " 建立会话...")
        else:
            friends = []
            selfId = ''
            for item in waiters_g:
                if(item.get('self') == self):
                    friends = item.get('friends')
                    selfId = item.get('selfId')
                    break
            for friendId in friends:
                friendItem = self.existFriend(friendId)
                if(friendItem != 0):
                    friendItem.get('self').write_message(message, True)

    def existFriend(self, friendId):
        for item in waiters_g:
            if(item.get('selfId') == friendId):
                return item
        return 0
        
    def on_close(self):
        """
        客户端关闭连接时，，自动执行
        :return: 
        """
        print('close', self.close_code, '--', self.close_reason)
        friends = []
        for item in waiters_g:
            if(item.get('self') == self):
                friends = item.get('friends')
                waiters_g.remove(item)
                
        for friendId in friends:
                friendItem = self.existFriend(friendId)
                if(friendItem != 0):
                    friendItem.get('self').close()       


def run(host='0.0.0.0', port=8080):
    asyncio.set_event_loop(asyncio.new_event_loop())
    application = tornado.web.Application([
        ("/websocket", ChatHandler),
    ])
    https_server = tornado.httpserver.HTTPServer(application, ssl_options={
        "certfile": '/root/vuePro_yujian/server/key/top.pem',
        "keyfile": '/root/vuePro_yujian/server/key/top.key',

    })
    https_server.listen(port, host)
    
    print('websocket开启: ', host, ':', port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
  run()
