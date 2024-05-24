import request from '@/utils/axios'

export function login (body) {
  return request({
    url: '/api/system/auth/login',
    method: 'post',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    data: body
  })
}

export function getNewToken (body) {
  return request({
    url: '/api/system/auth/token/refresh',
    method: 'post',
    data: body
  })
}

export function getCaptcha () {
  return request({
    url: '/api/system/auth/captcha/get',
    method: 'post',
  })
}
