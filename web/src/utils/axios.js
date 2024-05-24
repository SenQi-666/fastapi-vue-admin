import axios from 'axios'
import storage from 'store'
import router from '@/router'
import { getNewToken } from '@/api/auth.js'
import { save_token } from "./util.js"
import notification from 'ant-design-vue/es/notification'

const apiUrl = import.meta.env.VITE_API_BASE_URL;

// 创建 axios 实例
const request = axios.create({
  baseURL: apiUrl,
  timeout: 10000 // 请求超时时间
})

// 异常拦截处理器
const errorHandler = async (error) => {
  if (!error.response) {
    return Promise.reject(error)
  }

  const data = error.response.data
  // 从 localstorage 获取 access_token
  const access_token = storage.get('Access-Token')

  if (data.code === 403) {
    storage.remove('Access-Token');
    storage.remove('Refresh-Token');

    notification.error({
      message: '错误',
      description: data.message
    })
    router.push('/login')
    return Promise.reject(error)
  }

  if (data.code === 401) {
    if (!access_token) {
      notification.error({
        message: '错误',
        description: data.message
      })
      router.push('/login')
      return Promise.reject(error)
    }

    const refresh_token = storage.get('Refresh-Token')
    storage.remove('Access-Token');
    storage.remove('Refresh-Token');

    return getNewToken({ refresh_token: refresh_token }).then(response => {
      const result = response.data;
      if (result.code === 200) {
        save_token(result.data.access_token, result.data.refresh_token, result.data.expires_in)
        return request(error.response.config).then(response => response)
      }

      notification.error({
        message: '错误',
        description: result.message
      })
      router.push('/login')
      return Promise.reject(error)
    })
    .catch(error => {
      notification.error({
        message: '错误',
        description: data.message
      })
      return Promise.reject(error)
    });
  } else {
    notification.error({
      message: '错误',
      description: data.message
    })
    return Promise.reject(error)
  }
}

// 请求拦截器
request.interceptors.request.use(config => {
  const token = storage.get('Access-Token')
  // 如果 token 存在
  // 让每个请求携带自定义 token 请根据实际情况自行修改
  if (token) {
    config.headers['Authorization'] = 'Bearer ' + token
  }
  return config
}, errorHandler)

// 响应拦截器
request.interceptors.response.use(response => {
  if (response.data.code !== 200) {
    notification.error({
      message: '错误',
      description: response.data.message
    })
    return Promise.reject(response)
  }
  return response
}, errorHandler)

export default request