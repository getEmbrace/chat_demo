import axios from 'axios'

function request(config){
  const instance = axios.create({
    // baseURL: 'http://127.0.0.1:8081',
    timeout: 5000
  })

  //请求拦截
  instance.interceptors.request.use(config => {

    return config
  })
  //响应拦截
  instance.interceptors.response.use(res => {
    if(res.headers['content-type'] == 'video/webm'){
      return [res.data, 1]
    }
    return res.data
  })
  return instance(config)
}

export default request