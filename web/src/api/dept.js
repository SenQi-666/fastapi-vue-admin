import request from '@/utils/axios'

export function getDeptList () {
  return request({
    url: '/api/system/dept/list',
    method: 'get'
  })
}

export function getDeptOptions () {
  return request({
    url: '/api/system/dept/options',
    method: 'get'
  })
}

export function createDept (body) {
  return request({
    url: '/api/system/dept/create',
    method: 'post',
    data: body
  })
}

export function updateDept (body) {
  return request({
    url: '/api/system/dept/update',
    method: 'post',
    data: body
  })
}

export function deleteDept (parameter) {
  return request({
    url: '/api/system/dept/delete',
    method: 'post',
    params: parameter
  })
}

export function batchEnableDept (body) {
  return request({
    url: '/api/system/dept/batch/enable',
    method: 'post',
    data: body
  })
}

export function batchDisableDept (body) {
  return request({
    url: '/api/system/dept/batch/disable',
    method: 'post',
    data: body
  })
}