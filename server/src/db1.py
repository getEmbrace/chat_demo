
import pymysql
import os
import datetime

myBaseUser = {'host': 'localhost', 'dbName': 'xxxxxx',
              'username': 'root', 'password': 'xxxxxx'}


class MyDb:

    def __init__(self, host, user, password, dbName) -> None:
        self.host = host
        self.user = user
        self.password = password
        self.dbName = dbName
        self.conn = None
        self.cursor = None
        self.status = None
        self.connect()

    def connect(self):
        # 创建连接
        try:
            self.conn = pymysql.connect(host=self.host, user=self.user,
                                        password=self.password)
            self.conn.close()
        except:
            print("数据库连接失败(密码用户名错误 或 mysql服务器未开启)...")
            self.status = -1
            self.conn = None
            return
        try:
            self.conn = pymysql.connect(host=self.host, user=self.user,
                                        password=self.password, db=self.dbName)
        except:
            print("数据库连接失败(数据库不存在)...")
            self.conn = pymysql.connect(host=self.host, user=self.user,
                                        password=self.password)
            self.status = 0
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            return

        # print("数据库连接成功...")
        self.status = 1
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 创建数据库
    def createDb(self):

        sql = "CREATE DATABASE IF NOT EXISTS {}".format(self.dbName)
        self.cursor.execute(sql)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        self.connect()

    # 删除数据库
    def deleteDb(self):
        sql = "DROP DATABASE IF EXISTS {}".format(self.dbName)
        self.cursor.execute(sql)
        self.conn.commit()
    # 删除数据表

    def delTable(self, tableName):
        sql = "DROP TABLE IF EXISTS {}".format(tableName)
        self.cursor.execute(sql)
        self.conn.commit()

    # 新建表
    def createTable(self, TbAttribute):
        # 构建SQL
        tableName = TbAttribute.get("tableName")
        sql = "CREATE TABLE IF NOT EXISTS `{}`(".format(tableName)
        field = TbAttribute.get("field")
        where = TbAttribute.get("where")
        for item in field:
            # 字段
            sqlTem = "`{}` {},".format(item, field.get(item))
            sql = sql + sqlTem

        sql = sql + "PRIMARY KEY ( `{}` )".format(where)
        sql = sql + ")ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
        self.cursor.execute(sql)
        self.conn.commit()

    # 增删改查
    def addData(self, TbAttribute):
        # 构建SQL
        try:
            tableName = TbAttribute.get("tableName")
            sql = "INSERT INTO {tableName}(".format(tableName=tableName)
            field = TbAttribute.get("field")
            for item in field:
                # 字段
                sql = sql + item + ','
            sql = sql[:-1] + ') values('
            for item1 in field:
                # 数据
                sql = sql + '"' + field.get(item1) + '"' + ','
            sql = sql[:-1] + ')'

            self.cursor.execute(sql)
            self.conn.commit()
        except:
            print("error:", sql)
            return 0
        return 1

    def delData(self, TbAttribute):
        # 构建SQL
        tableName = TbAttribute.get("tableName")
        where = TbAttribute.get("where")
        sql = "DELETE FROM {tableName} WHERE {where}".format(
            tableName=tableName,
            where=where
        )
        self.cursor.execute(sql)
        self.conn.commit()

    def upData(self, TbAttribute):
        # 构建SQL
        tableName = TbAttribute.get("tableName")
        field = TbAttribute.get("field")
        where = TbAttribute.get("where")
        sql = "UPDATE {tableName} SET ".format(tableName=tableName)
        for item in field:
            sqlTem = item + "=" + '"' + field.get(item) + '"' + ","
            sql = sql + sqlTem

        sql = sql[:-1] + " WHERE " + where
        # print(sql)
        self.cursor.execute(sql)
        self.conn.commit()

    def selectData(self, TbAttribute):
        # 构建SQL
        tableName = TbAttribute.get("tableName")
        field = TbAttribute.get("field")
        where = TbAttribute.get("where")
        sql = "SELECT "
        for item in field:
            sql = sql + item + ','

        sql = sql[:-1] + " FROM {tableName} WHERE {where}".format(
            tableName=tableName,
            where=where
        )
        # print(sql)
        data = None
        try:
            if self.cursor.execute(sql):
                data = self.cursor.fetchall()
        except:
            data = None
        return data

    # 退出
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        # print("关闭链接")


class SetKey:
    def __init__(self) -> None:
        self.Key = True

    def openKey(self):
        if(self.Key == False):
            while(1):
                if(self.Key):
                    break
        self.Key = False

    def closeKey(self):
        self.Key = True


def OpenDb(username, password):
    con = MyDb(host=myBaseUser.get('host'), user=username,
               password=password, dbName=myBaseUser.get('dbName'))
    if con.status == -1:
        # print("mysql未开启服务...")
        return -1
    elif(con.status == 1):
        return con
    elif(con.status == 0):
        con.close()
        print("mysql数据库不存在...")
        return 0


# 操作数据库函数
#type: 0 / selectData
#type: 1 / addDate
#type: 2 / delData
#type: 3 / upData
Key = SetKey()


def useDb(table, where, field, sql=None,
          Dbuser={'username': myBaseUser.get('username'), 
                  'password': myBaseUser.get('password')},
                    type=0, isKey=False):
    if(isKey):
        Key.openKey()
    connect = OpenDb(Dbuser.get('username'), Dbuser.get('password'))
    # 判断数据库连接成功
    if(connect != 0 and connect != -1):
        if(sql == None):
            methods = [connect.selectData, connect.addData,
                       connect.delData, connect.upData]
            TbAttribute = {
                "tableName": "{}".format(table),
                "where": where,
                "field": field
            }
            Info = methods[type](TbAttribute)
            connect.close()
        else:
            try:
                connect.cursor.execute(sql)
                connect.conn.commit()
                connect.close()
                Info = 1
            except:
                connect.close()
                Info = 0
    else:
        if(isKey):
            Key.closeKey()
        return 0

    if(isKey):
        Key.closeKey()
    return Info


def getDbuser(where):
    userInfo = useDb('user', where, {"username": "", "password": ""})
    if(userInfo):
        return userInfo[0]
    else:
        return 0


def init():
    import os
    import datetime
    con = MyDb(host=myBaseUser.get('host'), user=myBaseUser.get('username'),
               password=myBaseUser.get('password'), dbName=myBaseUser.get('dbName'))
    if(con.conn and con.status == 0):
        con.createDb()

        TbAttribute = {"tableName": "fileaddr",
                       "field": {"id": "INT UNSIGNED AUTO_INCREMENT",
                                 "type": "VARCHAR(50) NOT NULL",
                                 "VirtualAddress": "VARCHAR(50) NOT NULL",
                                 "AbsoluteAddress": "VARCHAR(100) NOT NULL",
                                 "firstTime": "VARCHAR(50) NOT NULL"
                                 },
                       "where": "id"
                       }
        con.createTable(TbAttribute)

        TbAttribute = {"tableName": "message",
                       "field": {"id": "INT UNSIGNED AUTO_INCREMENT",
                                 "origin": "VARCHAR(50) NOT NULL",
                                 "dest": "VARCHAR(50) NOT NULL",
                                 "content": "VARCHAR(1000)",
                                 "destKind": "smallint(6) NOT NULL DEFAULT '0'",
                                 "originKind": "smallint(6) NOT NULL DEFAULT '0'",
                                 "Kind": "smallint(6) NOT NULL DEFAULT '1'",
                                 },
                       "where": "id"
                       }
        con.createTable(TbAttribute)

        TbAttribute = {"tableName": "user",
                       "field": {"id": "INT UNSIGNED AUTO_INCREMENT",
                                    "username": "VARCHAR(50) NOT NULL",
                                    "password": "VARCHAR(50) NOT NULL",
                                    "email": "VARCHAR(100)",
                                    "cooike": "VARCHAR(100)",
                                    "lastTime": "DATETIME",
                                    "firstTime": "DATETIME",
                                    "extend": "VARCHAR(800)",
                                    "friends": "varchar(800) DEFAULT NULL",
                                    "active": "smallint(6) DEFAULT '0'",
                                    "picture": "varchar(100) DEFAULT '/resource/image/userPic/default.jpg'",
                                    "sex": "varchar(10) DEFAULT '女'",
                                    "age": "varchar(50) DEFAULT '20'",
                                    "birthday": "varchar(50) DEFAULT '2021-8-8'",
                                    "cons": "varchar(30) DEFAULT '狮子座'",
                                    "signature_m": "varchar(100) DEFAULT '世界那么大，我想去看看'",
                                    "selectedPic": "varchar(100) DEFAULT '/resource/image/userPic/default.jpg'",
                                 },
                       "where": "id"
                       }
        con.createTable(TbAttribute)
        # 遍历资源文件
        for root, dirs, files in os.walk("/root/vuePro_yujian/server/dist"):
            # print(root, end=' ')    # 当前目录路径
            # print(dirs, end=' ')    # 当前路径下的所有子目录
            # print(files)          # 当前目录下的所有非目录子文件
            for item in files:
                path = root + "/" + item
                AbsoluteAddress = path.replace('\\', '/')
                VirtualAddress = AbsoluteAddress.split('dist')[1]
                type = path.split('.')[-1]
                print(type, VirtualAddress, AbsoluteAddress)
                TbAttribute = {"tableName": "fileaddr",
                               "field": {
                                            "type": type,
                                            "VirtualAddress": VirtualAddress,
                                            "AbsoluteAddress": AbsoluteAddress,
                                            "firstTime": str(datetime.datetime.today())
                               }
                               }
                con.addData(TbAttribute)

        con.close()
    else:
        print("初始化数据库失败...")


if __name__ == "__main__":
   # init()

    for root, dirs, files in os.walk("/root/vuePro_yujian/server/dist"):
        # print(root, end=' ')    # 当前目录路径
        # print(dirs, end=' ')    # 当前路径下的所有子目录
        # print(files)          # 当前目录下的所有非目录子文件
        for item in files:
            path = root + "/" + item
            AbsoluteAddress = path.replace('\\', '/')
            VirtualAddress = AbsoluteAddress.split('dist')[1]
            type = path.split('.')[-1]
            print(type, VirtualAddress, AbsoluteAddress)
            TbAttribute = {
                "type": type,
                "VirtualAddress": VirtualAddress,
                "AbsoluteAddress": AbsoluteAddress,
                "firstTime": str(datetime.datetime.today())
            }
            addrInfo = useDb('fileaddr', "VirtualAddress='{}'".format(
                VirtualAddress), {"AbsoluteAddress": ""})
            if(addrInfo):
                useDb('fileaddr', "VirtualAddress='{}'".format(
                    VirtualAddress), {"AbsoluteAddress": ""}, type=2)

            useDb('fileaddr', "VirtualAddress='{}'".format(
                VirtualAddress), TbAttribute, type=1)

    '''
    for root, dirs, files in os.walk("/root/vuePro_yujian/server/dist"):
         #print(root, end=' ')    # 当前目录路径
        # print(dirs, end=' ')    # 当前路径下的所有子目录
        #print(files)            # 当前目录下的所有非目录子文件
        for item in files:
            path = root + "/" +item
            AbsoluteAddress = path.replace('\\', '/')
            VirtualAddress = AbsoluteAddress.split('dist')[1]
            types = path.split('.')[-1]
            print(types,VirtualAddress,AbsoluteAddress)
            TbAttribute = {"tableName": "fileaddr",
                            "field": {
                                        "type": types,
                                        "VirtualAddress": VirtualAddress,
                                        "AbsoluteAddress": AbsoluteAddress,
                                        "firstTime": str(datetime.datetime.today())
                                        }
                            }
            con.addData(TbAttribute)
    con.close()
    '''
    '''
    con.delTable('fileAddr')
    TbAttribute = {"tableName": "fileaddr",
                    "field": {"id": "INT UNSIGNED AUTO_INCREMENT",
                              "type": "VARCHAR(50) NOT NULL",
                              "VirtualAddress": "VARCHAR(50) NOT NULL",
                              "AbsoluteAddress": "VARCHAR(50) NOT NULL",
                              "firstTime": "VARCHAR(50) NOT NULL"
                             },
                 "where": "id"
                }
    con.createTable(TbAttribute)
    '''

    # TbAttribute = {"tableName": "goods",
    #                "field": {"id": "INT UNSIGNED AUTO_INCREMENT",
    #                          "Name": "VARCHAR(20) NOT NULL",
    #                          "price": "INT NOT NULL",
    #                          "description": "VARCHAR(100)",
    #                          "onShelf": "TINYINT",
    #                          "lastTime": "DATETIME",
    #                          "firstTime": "DATETIME",
    #                          "extend": "VARCHAR(200)",
    #                         },
    #                "where": "id"
    #                }
    # con.createTable(TbAttribute)
    # TbAttribute = {"tableName": "message",
    #                "field": {"id": "INT UNSIGNED AUTO_INCREMENT",
    #                          "origin": "VARCHAR(50) NOT NULL",
    #                          "dest": "VARCHAR(50) NOT NULL",
    #                          "content": "VARCHAR(1000)",
    #                         },
    #                "where": "id"
    #                }
    # con.createTable(TbAttribute)
    # TbAttribute = {"tableName": "user",
    #                "field": {"id": "INT UNSIGNED AUTO_INCREMENT",
    #                          "username": "VARCHAR(20) NOT NULL",
    #                          "password": "INT NOT NULL",
    #                          "email": "VARCHAR(100)",
    #                          "passwordQuestion": "VARCHAR(100)",
    #                          "passwordAnswer": "VARCHAR(100)",
    #                          "cookie": "VARCHAR(100)",
    #                          "lastTime": "DATETIME",
    #                          "firstTime": "DATETIME",
    #                          "extend": "VARCHAR(800)",
    #                         },

    #                "where": "id"
    #                }
    # con.createTable(TbAttribute)

    # os.walk()遍历文件夹下的所有文件
    # os.walk()获得三组数据(rootdir, dirname,filnames)
    '''
    TbAttribute = {"tableName": "fileaddr",
                 "field": {
                             "type": "jpg",
                             "VirtualAddress": "/resource/image/userPic/default.jpg",
                             "AbsoluteAddress": "/root/vuePro_yujian/server/resource/image/userPic/default.jpg",
                             "firstTime": str(datetime.datetime.today())
                             }
                 }
    con.addData(TbAttribute)
    
    '''
    # for i in range(30):
    #     TbAttribute = {"tableName": "goods",
    #                 "field": {
    #                             "Name": "西游记"+ str(i),
    #                             "price": str(100+i),
    #                             "description": "经典读物《西游记》",
    #                             "spic": "/resource/index/image/download3.png",
    #                             "bpic": "/resource/index/image/download3.png",
    #                 }
    #                 }
    #     con.addData(TbAttribute)
    # TbAttribute = {"tableName": "goods",
    #                 "field": {
    #                             "Name": "西游记",
    #                             "price": "100",
    #                             "description": "经典读物《西游记》",
    #                             "spic": "/resource/index/image/download3.png",
    #                             "bpic": "/resource/index/image/download3.png",
    #                 }
    #             }
    # con.addData(TbAttribute)

    # TbAttribute = {
    #     "tableName": "user",
    #     "field": ["username", "测试1"]
    # }
    # con.delData(TbAttribute)
    # TbAttribute = {
    #     "tableName": "goods",
    #     "where":'Name = "12西游记"',
    #     "field": {
    #                 "spic": "/resource/index/image/download2.jpg",
    #                 "bpic": "/resource/index/image/download2.jpg",
    #               }
    # }
    # con.upData(TbAttribute)
    # TbAttribute = {
    #     "tableName": "user",
    #     "where":["username", "测试3"],
    #     "field": {"username": "测试3",
    #               "password": "123456"
    #               }
    # }
    # data = con.selectData(TbAttribute)
    # print(data)

    # con.close()
