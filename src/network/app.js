import request from './index.js'

export function setActive(cooike, active){
  return request({
    url: 'setActive',
    method: 'post',
    data: {
      cooike,
      active
    }
  })
}
export function closeLongSrc(cooike, url){
  return request({
    url: '/closeLongSrc',
    method: 'post',
    data: {
      cooike,
      url
    }
  })
}
export function setMessageStatus(cooike, messageId){
  return request({
    url: '/setMessageStatus',
    method: 'post',
    data: {
      cooike,
      messageId
    }
  })
}