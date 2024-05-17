import request from '@/utils/axios'

export function getPositionList (parameter) {
  return request({
    url: '/api/system/position/list',
    method: 'get',
    params: parameter
  })
}

export function getPositionOptions (parameter) {
  return request({
    url: '/api/system/position/options',
    method: 'get',
    params: parameter
  })
}

export function createPosition (body) {
  return request({
    url: '/api/system/position/create',
    method: 'post',
    data: body
  })
}

export function updatePosition (body) {
  return request({
    url: '/api/system/position/update',
    method: 'post',
    data: body
  })
}

export function deletePosition (parameter) {
  return request({
    url: '/api/system/position/delete',
    method: 'post',
    params: parameter
  })
}

export function batchEnablePosition (body) {
  return request({
    url: '/api/system/position/batch/enable',
    method: 'post',
    data: body
  })
}

export function batchDisablePosition (body) {
  return request({
    url: '/api/system/position/batch/disable',
    method: 'post',
    data: body
  })
}