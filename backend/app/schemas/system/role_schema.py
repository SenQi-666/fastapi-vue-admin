#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Optional, List
from pydantic import BaseModel, ConfigDict, model_validator
from app.core.validator import role_permission_request_validator
from app.schemas.system import MenuSimpleOut, MenuOptionsOut, DeptOptionsOut
from app.schemas.base import CustomOutSchema


class Role(BaseModel):
    name: str
    order: Optional[int] = 1
    description: Optional[str] = None


class RoleCreate(Role):
    ...


class RoleUpdate(Role):
    id: int
    available: Optional[bool]


class RoleBatchSetAvailable(BaseModel):
    ids: List[int] = []


class RolePermissionSetting(BaseModel):
    role_ids: List[int] = []
    menu_ids: List[int] = []
    data_scope: int = 1
    dept_ids: List[int] = []

    @classmethod
    @model_validator(mode='after')
    def validate_fields(cls, data):
        return role_permission_request_validator(data)


class RoleOut(Role, CustomOutSchema):
    data_scope: int = 1
    available: Optional[bool]


class RoleSimpleOut(RoleOut):
    data_scope: int = 1
    menus: List[MenuOptionsOut] = []


class RoleOptionsOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str] = None
    available: Optional[bool]


class RolePermissionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    data_scope: int = 1
    menus: List[MenuOptionsOut] = []
    depts: List[DeptOptionsOut] = []
    available: Optional[bool]


class RolePermissionSimpleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    data_scope: int = 1
    menus: List[MenuSimpleOut] = []
    depts: List[DeptOptionsOut] = []
    available: Optional[bool]
