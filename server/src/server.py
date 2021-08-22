
from socket import *
import threading
import datetime
import ssl

import myHttp
import db1 as DB
import root
import websocketServer as ws

useDb = DB.useDb

class Server:
    def __init__(self, IP, Port, routers):
        self.IP = IP
        self.Port = Port
        self.routers = routers
        self.context = None
    def Resources(self, requestInfo):
        url = requestInfo['url']
        #连接数据库
        addrInfo = useDb('fileaddr', "VirtualAddress='{}'".format(url), 
              {"type": "", "AbsoluteAddress": ""})
        if(addrInfo):
            content_type = 'text/html'
            filetype = addrInfo[0].get('type')
            AbsoluteAddress = addrInfo[0].get('AbsoluteAddress')
            try:
                if(filetype == "jpg" or filetype == "png"or filetype == "ico"or filetype == "jpeg"):
                    with open(r"{}".format(AbsoluteAddress), 'rb') as f:
                        data = f.read()
                    content_type = 'image/{}'.format(filetype)
                else:
                    with open(r"{}".format(AbsoluteAddress), 'r', encoding='utf-8') as f:
                        data = f.read()
                    content_type = 'text/{}'.format(filetype)
                    
                response = myHttp.response({
                    'headers': {
                        'Content-Type': content_type
                    },
                    'body': data
                })
                # print(respon)
                return response
            except:
                print(2)
                return myHttp.response({'status': 404})
        else:
            return myHttp.response({'status': 404})
        
    def HeaderLength(self, request):
        itemList = request.split('\r\n\r\n', 1)
        if(len(itemList) == 1):
            headers, bodys = itemList[0], ""
            return 0
        else:
            headers, bodys = itemList[0], itemList[1]
            return len(headers) + 4
        
    def Threadfun(self, conn, addr):
        g_length = 0
        userHttp = myHttp.requestInfo
        userHttp_from = myHttp.request_form
        data_b = conn.recv(1024)
        requestInfo = userHttp(str(data_b.split(b'\r\n\r\n')[0], encoding='utf-8'))
        headerLength = self.HeaderLength(data_b.decode('utf-8', 'ignore'))
        c_length = requestInfo['field'].get('Content-Length')
        conent_type = requestInfo['field'].get('Content-Type')
        g_length = len(data_b)
        if(c_length):
            c_length = int(c_length) + headerLength
            while(True):
                if(g_length >= c_length):
                    break
                data_b = data_b + conn.recv(4096)
                g_length = len(data_b)
                if(g_length >= c_length): 
                    break
        if(conent_type and conent_type.split(';')[0] == "multipart/form-data"):
            requestInfo = userHttp_from(data_b)
        else:  
            requestInfo = userHttp(str(data_b, encoding='utf-8'))
            
        url = requestInfo['url']
        method = requestInfo['method']
        if(url == ''):
            conn.close()
            return

        print("\nTime: {}\n\t连接来自{},url:{}, method:{}".format(datetime.datetime.today(), addr, url, method))
        if(method == "OPTIONS"):
            response = myHttp.response({})
        else:   
            response = self.routers.get(url, self.Resources)(requestInfo)
    
        conn.send(response)
        conn.close()

    def setSSL(self, certfile, keyfile):
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain(certfile=certfile, keyfile=keyfile)
        self.context = context

    def run(self):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind((self.IP, self.Port))
        sock.listen(100)
        print("开启服务: ",self.IP,':',self.Port)
        while True:
            conn, addr = sock.accept()
            if(self.context != None):
                connstream = self.context.wrap_socket(conn, server_side=True)
            else:
                connstream = conn
            t = threading.Thread(target = self.Threadfun, args = (connstream, addr, ))
            t.setDaemon(True)
            t.start()
            

if __name__ == "__main__":
    server = Server("0.0.0.0",443, root.routers)
    t = threading.Thread(target = ws.run, args=('0.0.0.0', '8080', ))
    t.setDaemon(True)
    t.start()
    server.setSSL('/root/vuePro_yujian/server/key/top.pem', '/root/vuePro_yujian/server/key/top.key')
    server.run()
