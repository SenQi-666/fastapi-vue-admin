#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from app.core.router_class import OperationLogRoute
from app.core.dependencies import AuthPermission
from app.services.system import DeptService
from app.utils.response import SuccessResponse
from app.schemas.system import (
    Auth,
    DeptCreate,
    DeptUpdate,
    DeptBatchSetAvailable
)


router = APIRouter(route_class=OperationLogRoute)


@router.get("/list", summary="查询部门", description="查询部门")
async def get_dept_list(
        auth: Auth = Depends(AuthPermission(permissions=["system:dept:query"])),
) -> JSONResponse:
    data = await DeptService.get_dept_list(auth)
    return SuccessResponse(data)


@router.get("/detail", summary="查询部门详情", description="查询部门详情")
async def get_dept_detail(
        id: int = Query(..., description="部门ID"),
        auth: Auth = Depends(AuthPermission(permissions=["system:dept:query"])),
) -> JSONResponse:
    data = await DeptService.get_dept_detail(id, auth)
    return SuccessResponse(data)


@router.get("/options", summary="查询部门选项", description="查询部门选项")
async def get_dept_options(
        auth: Auth = Depends(AuthPermission(permissions=["system:dept:options"])),
) -> JSONResponse:
    data = await DeptService.get_dept_options(auth)
    return SuccessResponse(data)


@router.post("/create", summary="创建部门", description="创建部门")
async def create_dept(
        dept_in: DeptCreate,
        auth: Auth = Depends(AuthPermission(permissions=["system:dept:create"])),
) -> JSONResponse:
    data = await DeptService.create_dept(dept_in, auth)
    return SuccessResponse(data, msg="创建成功")


@router.post("/update", summary="修改部门", description="修改部门")
async def update_dept(
        dept_in: DeptUpdate,
        auth: Auth = Depends(AuthPermission(permissions=["system:dept:update"])),
) -> JSONResponse:
    data = await DeptService.update_dept(dept_in, auth)
    return SuccessResponse(data, msg="修改成功")


@router.post("/delete", summary="删除部门", description="删除部门")
async def delete_dept(
        id: int = Query(..., description="部门ID"),
        auth: Auth = Depends(AuthPermission(permissions=["system:dept:delete"])),
) -> JSONResponse:
    await DeptService.delete_dept(id, auth)
    return SuccessResponse(msg="删除成功")


@router.post("/batch/enable", summary="批量启用菜单", description="批量启用菜单")
async def batch_enabled_dept(
        data: DeptBatchSetAvailable,
        auth: Auth = Depends(AuthPermission(permissions=["system:dept:update"])),
) -> JSONResponse:
    await DeptService.enable_dept(data.ids, auth)
    return SuccessResponse(msg="启用成功")


@router.post("/batch/disable", summary="批量停用菜单", description="批量停用菜单")
async def batch_disable_dept(
        data: DeptBatchSetAvailable,
        auth: Auth = Depends(AuthPermission(permissions=["system:dept:update"])),
) -> JSONResponse:
    await DeptService.disable_dept(data.ids, auth)
    return SuccessResponse(msg="停用成功")
