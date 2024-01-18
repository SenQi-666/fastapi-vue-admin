#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.core.router_class import OperationLogRoute
from app.core.params import PaginationQueryParams, LogQueryParams
from app.core.dependencies import AuthPermission
from app.services.system import LogService
from app.utils.response import SuccessResponse, PaginationResponse
from app.schemas.system import Auth


router = APIRouter(route_class=OperationLogRoute)


@router.get("/list", summary="查询操作日志", description="查询操作日志")
async def get_user_list(
        paging_query: PaginationQueryParams = Depends(),
        log_query: LogQueryParams = Depends(),
        auth: Auth = Depends(AuthPermission(permissions=["system:log:query"])),
) -> JSONResponse:
    search = log_query.__dict__
    data = await LogService.get_log_list(search, auth)
    return PaginationResponse(data, page=paging_query.page, page_size=paging_query.page_size)
