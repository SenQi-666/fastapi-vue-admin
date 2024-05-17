import request from '@/utils/axios'

export function getLogList (parameter) {
  return request({
    url: '/api/system/log/list',
    method: 'get',
    params: parameter
  })
}