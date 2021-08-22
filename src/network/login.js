import request from './index.js'

export function login(username='test', password='test') {
  return request({
    url: '/login',
    method: 'post',
    data: {
      username,
      password
    }
  })
}
export function regist(username='test', password='test', email="2424535987@qq.com") {
  return request({
    url: '/regist',
    method: 'post',
    data: {
      username,
      password,
      email
    }
  })
}