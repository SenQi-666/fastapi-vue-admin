#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import APIRouter
from .auth import router as AuthRouter
from .menu import router as MenuRouter
from .dept import router as DeptRouter
from .position import router as PositionRouter
from .role import router as RoleRouter
from .user import router as UserRouter
from .log import router as LogRouter


SystemRouter = APIRouter()

SystemRouter.include_router(AuthRouter, prefix="/auth", tags=["系统认证"])
SystemRouter.include_router(MenuRouter, prefix="/menu", tags=["菜单模块"])
SystemRouter.include_router(DeptRouter, prefix="/dept", tags=["部门模块"])
SystemRouter.include_router(PositionRouter, prefix="/position", tags=["岗位模块"])
SystemRouter.include_router(RoleRouter, prefix="/role", tags=["角色模块"])
SystemRouter.include_router(UserRouter, prefix="/user", tags=["用户模块"])
SystemRouter.include_router(LogRouter, prefix="/log", tags=["操作日志"])
