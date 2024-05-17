#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from app.core.router_class import OperationLogRoute
from app.core.dependencies import AuthPermission
from app.services.system import MenuService
from app.utils.response import SuccessResponse
from app.schemas.system import (
    Auth,
    MenuCreate,
    MenuUpdate,
    MenuBatchSetAvailable
)


router = APIRouter(route_class=OperationLogRoute)


@router.get("/list", summary="查询菜单", description="查询菜单")
async def get_menu_list(
        auth: Auth = Depends(AuthPermission(permissions=["system:menu:query"], check_data_scope=False)),
) -> JSONResponse:
    data = await MenuService.get_menu_list(auth)
    return SuccessResponse(data)


@router.get("/detail", summary="查询菜单详情", description="查询菜单详情")
async def get_menu_detail(
        id: int = Query(..., description="菜单ID"),
        auth: Auth = Depends(AuthPermission(permissions=["system:menu:query"], check_data_scope=False)),
) -> JSONResponse:
    data = await MenuService.get_menu_detail(id, auth)
    return SuccessResponse(data)


@router.get("/options", summary="查询菜单选项", description="查询菜单选项")
async def get_menu_options(
        auth: Auth = Depends(AuthPermission(permissions=["system:menu:options"], check_data_scope=False)),
) -> JSONResponse:
    data = await MenuService.get_menu_options(auth)
    return SuccessResponse(data)


@router.post("/create", summary="创建菜单", description="创建菜单")
async def create_menu(
        menu_in: MenuCreate,
        auth: Auth = Depends(AuthPermission(permissions=["system:menu:create"], check_data_scope=False)),
) -> JSONResponse:
    data = await MenuService.create_menu(menu_in, auth)
    return SuccessResponse(data, msg="创建成功")


@router.post("/update", summary="修改菜单", description="修改菜单")
async def update_menu(
        menu_in: MenuUpdate,
        auth: Auth = Depends(AuthPermission(permissions=["system:menu:update"], check_data_scope=False)),
) -> JSONResponse:
    data = await MenuService.update_menu(menu_in, auth)
    return SuccessResponse(data, msg="修改成功")


@router.post("/delete", summary="删除菜单", description="删除菜单")
async def delete_menu(
        id: int = Query(..., description="菜单ID"),
        auth: Auth = Depends(AuthPermission(permissions=["system:menu:delete"], check_data_scope=False)),
) -> JSONResponse:
    await MenuService.delete_menu(id, auth)
    return SuccessResponse(msg="删除成功")


@router.post("/batch/enable", summary="批量启用菜单", description="批量启用菜单")
async def batch_enabled_menu(
        data: MenuBatchSetAvailable,
        auth: Auth = Depends(AuthPermission(permissions=["system:menu:update"], check_data_scope=False)),
) -> JSONResponse:
    await MenuService.enable_menu(data.ids, auth=auth)
    return SuccessResponse(msg="启用成功")


@router.post("/batch/disable", summary="批量停用菜单", description="批量停用菜单")
async def batch_disable_menu(
        data: MenuBatchSetAvailable,
        auth: Auth = Depends(AuthPermission(permissions=["system:menu:update"], check_data_scope=False)),
) -> JSONResponse:
    await MenuService.disable_menu(data.ids, auth=auth)
    return SuccessResponse(msg="停用成功")
