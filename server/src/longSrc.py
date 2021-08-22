import threading


class Mthread:
    def __init__(self, threadInfo):
        self.threadList = []
        self.threadList.append(threadInfo)

    # 需要表明用户及链接
    # threadInfo: {url, uid(标识), pro }
    # url: 当前链接， uid: 用户id，pro回调, event事件, isAlive线程挂起状态
    def appendThread(self, threadInfo):
        threadInfo['event'] = threading.Event()
        # 用于判断是否处于挂起
        threadInfo['isAlive'] = True
        # 用于判断是否主动退出: 1:主动退出 0:通过激活函数退出 -1:首次退出 
        threadInfo['exitKind'] = -1
        lastStatus = True
        
        for item in self.threadList:
            if(item.get('uid') == threadInfo.get('uid') and item.get('url') == threadInfo.get('url')):
                lastStatus = item.get('isAlive')
                if(item.get('isAlive')):
                    self.threadList.remove(item)
                    self.threadList.append(threadInfo)
                    self.watchThread(threadInfo)
                    threadInfo.get('event').wait()
                    # print(threadInfo.get('event'), 'alive')
                break
        if(lastStatus):   
            self.threadList.append(threadInfo)
        return threadInfo
    
    def existItem(self, uid, url):
        for item in self.threadList:
            if(item.get('uid') == uid and item.get('url') == url):
                return item
        return 0
    
    def end(self, uid, url):
        while(1):
            item = self.existItem(uid, url)
            if(item):
                self.threadList.remove(item)
            else:
                break
        
    def removeThread(self, uid, url):
        for item in self.threadList:
            if(item.get('uid') == uid and item.get('url') == url):
                item['isAlive'] = True
                item['exitKind'] = 1
                item.get('event').set()
                self.end(uid, url)
                print(item.get('threadName'), 'removed')

    def waitThread(self, uid, url):
        for item in self.threadList:
            if(item.get('uid') == uid and item.get('url') == url):
                item.get('event').wait()
                break

    def notifyThread(self, uid, url):
        for item in self.threadList:
            if(item.get('uid') == uid and item.get('url') == url):
                item['isAlive'] = True
                item.get('event').set()
                break

    def watchThread(self, threadInfo):
      alive = Alive(threadInfo)
      proThread = threading.Thread(target=threadInfo.get('pro'), args=(alive, ))
    #   proThread.setDaemon(True)
      proThread.start()

class Alive:
    def __init__(self, threadInfo):
        self.threadInfo = threadInfo
    
    def next(self):
        self.threadInfo['exitKind'] = 0
        self.threadInfo['isAlive'] = True
        self.threadInfo.get('event').set()
    
    def start(self):
        self.threadInfo['isAlive'] = False