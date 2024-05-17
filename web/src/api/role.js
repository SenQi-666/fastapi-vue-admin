import request from '@/utils/axios'

export function getRoleList (parameter) {
  return request({
    url: '/api/system/role/list',
    method: 'get',
    params: parameter
  })
}

export function getRoleOptions (parameter) {
  return request({
    url: '/api/system/role/options',
    method: 'get',
    params: parameter
  })
}

export function createRole (body) {
  return request({
    url: '/api/system/role/create',
    method: 'post',
    data: body
  })
}

export function updateRole (body) {
  return request({
    url: '/api/system/role/update',
    method: 'post',
    data: body
  })
}

export function deleteRole (parameter) {
  return request({
    url: '/api/system/role/delete',
    method: 'post',
    params: parameter
  })
}

export function batchEnableRole (body) {
  return request({
    url: '/api/system/role/batch/enable',
    method: 'post',
    data: body
  })
}

export function batchDisableRole (body) {
  return request({
    url: '/api/system/role/batch/disable',
    method: 'post',
    data: body
  })
}

export function getRolePermission (parameter) {
  return request({
    url: '/api/system/role/permission',
    method: 'get',
    params: parameter
  })
}

export function setPermission (body) {
  return request({
    url: '/api/system/role/permission/setting',
    method: 'post',
    data: body
  })
}