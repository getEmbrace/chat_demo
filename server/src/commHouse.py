import time

class CommHouse:
  def __init__(self) -> None:
      self.houseList = []
      
  def createHouse(self, Cmember):
    houseNum = int(time.time())
    self.houseList.append({
      "houseNum": houseNum,
      "Cmember": Cmember,
      "members": [Cmember],
      "message": {
        str(Cmember): [],
      }
    })
    return houseNum
  
  def delHouse(self, houseNum):
    house = self.getHouseByNum(houseNum)
    self.houseList.remove(house)
    return 1
  
  def appendMemberByC(self, Cmember, member):
    if(len(self.houseList) != 0):
      for house in self.houseList:
        if(house.get('Cmember') == Cmember):
          house.get('members').append(member)
          houseNum = house.get('houseNum')
          house.get('message')[str(member)] = []
          return [2, houseNum]
      houseNum = self.createHouse(member)
      return [1, houseNum]
    else:
      houseNum = self.createHouse(member)
      return [1, houseNum]
   
  def getHouseByNum(self, houseNum):
    for house in self.houseList:
      if(house.get('houseNum') == int(houseNum)):
        return house
    return 0
  
  def setMessage(self, houseNum, member, message):
    house = self.getHouseByNum(houseNum)
    if(house != 0):
      house.get('message')[str(member)].append(message)
      return 1
    else:
      return 0
   
  def getMessage(self, houseNum, member, count):
    house = self.getHouseByNum(houseNum)
    if(house != 0):
      messageList = house.get('message').get(str(member), None)
      if(len(messageList) == 0 ):
        message = 'None'
      elif(len(messageList) <= count):
        message = house.get('message').get(str(member), None)[0: ]
      elif(len(messageList) > count):
        message = house.get('message').get(str(member), None)[0: count]
        
      if(message != 'None'):
        for i in message:
          messageList.remove(i)
          
      return message
    else:
      return 0
  
  def getMesssgeLength(self, houseNum, member):
    house = self.getHouseByNum(houseNum)
    if(house != 0):
      messageList = house.get('message').get(str(member), None)
      return len(messageList)
    else:
      return 0
      
    
