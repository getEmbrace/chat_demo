import request from './index.js'

export function getMine(cooike){
  return request({
    url: '/getMine',
    method: 'post',
    data: {
      cooike
    }
  })
}
export function getFriends(cooike){
  return request({
    url: '/getFriends',
    method: 'post',
    timeout: 0,
    data: {
      cooike
    }
  })
}
export function getMessage_f(cooike, friendId){
  return request({
    url: '/getMessage_f',
    method: 'post',
    timeout: 0,
    data: {
      cooike,
      friendId
    }
  })
}
export function findUser(cooike, username){
  return request({
    url: '/findUser',
    method: 'post',
    data: {
      cooike,
      username
    }
  })
}
export function getUserInfo(uid){
  return request({
    url: '/getUserInfo',
    method: 'post',
    data: {
      uid
    }
  })
}
export function addFriend(cooike, addFriendId){
  return request({
    url: '/addFriend',
    method: 'post',
    data: {
      cooike,
      addFriendId
    }
  })
}
export function delFriend(cooike, delFriendId){
  return request({
    url: '/delFriend',
    method: 'post',
    data: {
      cooike,
      delFriendId
    }
  })
}
export function sendMessage(cooike, FriendId, message){
  return request({
    url: '/sendMessage',
    method: 'post',
    data: {
      cooike,
      FriendId,
      message
    }
  })
}
export function startLink_v(cooike, friendId){
  return request({
    url: '/startLink_v',
    method: 'post',
    timeout: 0,
    data: {
      cooike,
      friendId
    }
  })
}

export function commHouse(cooike, friendId, houseNum ){
  return request({
    url: '/commHouse',
    method: 'post',
    timeout: 0,
    responseType: 'blob',
    data: {
      cooike,
      friendId,
      houseNum
    }
  })
}
export function setHouseMessage(cooike, friendId, houseNum, message){
  let formData = new FormData();
  formData.append('cooike', cooike)
  formData.append('friendId', friendId)
  formData.append('houseNum', houseNum)
  formData.append('message', message)
  return request({
    url: '/setHouseMessage',
    method: 'post',
    timeout: 0,
    data: formData
  })
}

export function commWebsocket(cooike, friendId, callBack, url='wss://boygirl.top:8080/websocket'){
  let socket = new WebSocket(url)
  let init_message = {'cooike': cooike, 'friendId': friendId}
  socket.onopen = () => {
    socket.send(JSON.stringify(init_message))
    console.log(init_message);
    callBack && callBack(socket)
  }
  return socket
}