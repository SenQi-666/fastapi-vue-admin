#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, Query, UploadFile
from fastapi.responses import JSONResponse
from app.core.router_class import OperationLogRoute
from app.core.params import PaginationQueryParams, UserQueryParams
from app.core.dependencies import get_current_user, AuthPermission
from app.utils.response import SuccessResponse, PaginationResponse
from app.services.system import UserService
from app.schemas.system import (
    Auth,
    UserCreate,
    UserUpdate,
    CurrentUserUpdate,
    CurrentUserPasswordChange,
    UserBatchSetAvailable
)


router = APIRouter(route_class=OperationLogRoute)


@router.get("/current/info", summary="查询当前用户信息", description="查询当前用户信息")
async def get_current_user_info(auth: Auth = Depends(get_current_user)) -> JSONResponse:
    data = await UserService.get_current_user_info(auth)
    return SuccessResponse(data)


@router.post("/current/avatar/upload", summary="上传当前用户头像")
async def user_avatar_upload(file: UploadFile, auth: Auth = Depends(get_current_user)):
    avatar = await UserService.upload_avatar(file, auth)
    return SuccessResponse(avatar, msg='上传成功')


@router.post("/current/info/update", summary="更新当前用户基本信息", description="更新当前用户基本信息")
async def update_current_user_info(
        data: CurrentUserUpdate,
        auth: Auth = Depends(get_current_user)
) -> JSONResponse:
    data = await UserService.update_current_user_info(data, auth)
    return SuccessResponse(data, msg='更新成功')


@router.post("/current/password/change", summary="修改当前用户密码", description="修改当前用户密码")
async def change_current_user_password(
        data: CurrentUserPasswordChange,
        auth: Auth = Depends(get_current_user)
) -> JSONResponse:
    data = await UserService.change_user_password(data, auth)
    return SuccessResponse(data, msg='修改成功')


@router.get("/list", summary="查询用户", description="查询用户")
async def get_user_list(
        paging_query: PaginationQueryParams = Depends(),
        user_query: UserQueryParams = Depends(),
        auth: Auth = Depends(AuthPermission(permissions=["system:user:query"])),
) -> JSONResponse:
    search = user_query.__dict__
    data = await UserService.get_user_list(search, auth)
    return PaginationResponse(data, page=paging_query.page, page_size=paging_query.page_size)


@router.get("/detail", summary="查询用户详情", description="查询用户详情")
async def get_user_detail(
        id: int = Query(..., description="用户ID"),
        auth: Auth = Depends(AuthPermission(permissions=["system:user:query"])),
) -> JSONResponse:
    data = await UserService.get_detail_by_id(id, auth)
    return SuccessResponse(data)


@router.post("/create", summary="创建用户", description="创建用户")
async def create_user(
        user_in: UserCreate,
        auth: Auth = Depends(AuthPermission(permissions=["system:user:create"])),
) -> JSONResponse:
    data = await UserService.create_user(user_in, auth)
    return SuccessResponse(data, msg="创建成功")


@router.post("/update", summary="修改用户", description="修改用户")
async def update_user(
        user_in: UserUpdate,
        auth: Auth = Depends(AuthPermission(permissions=["system:user:update"])),
) -> JSONResponse:
    data = await UserService.update_user(user_in, auth)
    return SuccessResponse(data, msg="修改成功")


@router.post("/delete", summary="删除用户", description="删除用户")
async def delete_user(
        id: int = Query(..., description="用户ID"),
        auth: Auth = Depends(AuthPermission(permissions=["system:user:delete"])),
) -> JSONResponse:
    await UserService.delete_user(id, auth)
    return SuccessResponse(msg="删除成功")


@router.post("/batch/enable", summary="批量启用用户", description="批量启用用户")
async def batch_enabled_user(
        data: UserBatchSetAvailable,
        auth: Auth = Depends(AuthPermission(permissions=["system:user:update"])),
) -> JSONResponse:
    await UserService.set_user_available(data.ids, available=True, auth=auth)
    return SuccessResponse(msg="启用成功")


@router.post("/batch/disable", summary="批量停用用户", description="批量停用用户")
async def batch_disable_user(
        data: UserBatchSetAvailable,
        auth: Auth = Depends(AuthPermission(permissions=["system:user:update"])),
) -> JSONResponse:
    await UserService.set_user_available(data.ids, available=False, auth=auth)
    return SuccessResponse(msg="停用成功")
