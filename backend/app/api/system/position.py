#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from app.core.router_class import OperationLogRoute
from app.core.params import PaginationQueryParams, PositionQueryParams
from app.core.dependencies import AuthPermission
from app.services.system import PositionService
from app.utils.response import SuccessResponse, PaginationResponse
from app.schemas.system import (
    Auth,
    PositionCreate,
    PositionUpdate,
    PositionBatchSetAvailable
)


router = APIRouter(route_class=OperationLogRoute)


@router.get("/list", summary="查询岗位", description="查询岗位")
async def get_position_list(
        paging_query: PaginationQueryParams = Depends(),
        position_query: PositionQueryParams = Depends(),
        auth: Auth = Depends(AuthPermission(permissions=["system:position:query"])),
) -> JSONResponse:
    search = position_query.__dict__
    data = await PositionService.get_position_list(search, auth)
    return PaginationResponse(data, page=paging_query.page, page_size=paging_query.page_size)


@router.get("/detail", summary="查询岗位详情", description="查询岗位详情")
async def get_position_detail(
        id: int = Query(..., description="岗位ID"),
        auth: Auth = Depends(AuthPermission(permissions=["system:position:query"])),
) -> JSONResponse:
    data = await PositionService.get_position_detail(id, auth)
    return SuccessResponse(data)


@router.get("/options", summary="查询岗位选项", description="查询岗位选项")
async def get_position_options(
        paging_query: PaginationQueryParams = Depends(),
        position_query: PositionQueryParams = Depends(),
        auth: Auth = Depends(AuthPermission(permissions=["system:position:options"])),
) -> JSONResponse:
    search = position_query.__dict__
    data = await PositionService.get_position_options(search, auth)
    return PaginationResponse(data, page=paging_query.page, page_size=paging_query.page_size)


@router.post("/create", summary="创建岗位", description="创建岗位")
async def create_position(
        position_in: PositionCreate,
        auth: Auth = Depends(AuthPermission(permissions=["system:position:create"])),
) -> JSONResponse:
    data = await PositionService.create_position(position_in, auth)
    return SuccessResponse(data, msg="创建成功")


@router.post("/update", summary="修改岗位", description="修改岗位")
async def update_position(
        position_in: PositionUpdate,
        auth: Auth = Depends(AuthPermission(permissions=["system:position:update"])),
) -> JSONResponse:
    data = await PositionService.update_position(position_in, auth)
    return SuccessResponse(data, msg="修改成功")


@router.post("/delete", summary="删除岗位", description="删除岗位")
async def delete_position(
        id: int = Query(..., description="岗位ID"),
        auth: Auth = Depends(AuthPermission(permissions=["system:position:delete"])),
) -> JSONResponse:
    await PositionService.delete_position(id, auth)
    return SuccessResponse(msg="删除成功")


@router.post("/batch/enable", summary="批量启用岗位", description="批量启用岗位")
async def batch_enabled_position(
        data: PositionBatchSetAvailable,
        auth: Auth = Depends(AuthPermission(permissions=["system:position:update"])),
) -> JSONResponse:
    await PositionService.set_position_available(data.ids, available=True, auth=auth)
    return SuccessResponse(msg="启用成功")


@router.post("/batch/disable", summary="批量停用岗位", description="批量停用岗位")
async def batch_disable_position(
        data: PositionBatchSetAvailable,
        auth: Auth = Depends(AuthPermission(permissions=["system:position:update"])),
) -> JSONResponse:
    await PositionService.set_position_available(data.ids, available=False, auth=auth)
    return SuccessResponse(msg="停用成功")
