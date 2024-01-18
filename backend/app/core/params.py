#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Optional
from fastapi import Query
from app.core.validator import DateTimeStr


class PaginationQueryParams:
    """
    分页查询参数
    """
    def __init__(
            self,
            page: int = Query(1, description="页码"),
            page_size: int = Query(10, description="每页数量", ge=10, le=50)
    ) -> None:
        self.page = page
        self.page_size = page_size


class MenuQueryParams:
    """
    菜单管理查询参数
    """
    def __init__(self, available: Optional[bool] = Query(True, description="状态")) -> None:
        self.available = available


class DeptQueryParams:
    """
    部门管理查询参数
    """
    def __init__(self, available: Optional[bool] = Query(True, description="状态")) -> None:
        self.available = available


class PositionQueryParams:
    """
    岗位管理查询参数
    """
    def __init__(
            self,
            name: Optional[str] = Query(None, description="岗位名称"),
            available: Optional[bool] = Query(True, description="状态")
    ) -> None:
        self.name = ("like", name)
        self.available = available


class RoleQueryParams:
    """
    角色管理查询参数
    """
    def __init__(
            self,
            name: Optional[str] = Query(None, description="角色名称"),
            available: Optional[bool] = Query(True, description="状态")
    ) -> None:
        self.name = ("like", name)
        self.available = available


class UserQueryParams:
    """
    用户管理查询参数
    """
    def __init__(
            self,
            username: Optional[str] = Query(None, description="用户名"),
            name: Optional[str] = Query(None, description="姓名"),
            available: Optional[bool] = Query(True, description="状态")
    ) -> None:
        self.username = ("like", username)
        self.name = ("like", name)
        self.available = available

    def function(self, value):
        return value


class LogQueryParams:
    """
    操作日志查询参数
    """
    def __init__(
            self,
            request_path: Optional[str] = Query(None, description="请求路径"),
            creator: Optional[int] = Query(None, description="创建人"),
            start_time: Optional[DateTimeStr] = Query(None, description="开始时间"),
            end_time: Optional[DateTimeStr] = Query(None, description="结束时间"),
    ) -> None:
        self.request_path = ("like", request_path)
        self.creator_id = creator
        self.created_at = ("between", (start_time, end_time))
