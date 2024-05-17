#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Optional, List
from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from app.core.validator import DateTimeStr, mobile_validator
from app.schemas.system import RoleOptionsOut, RolePermissionSimpleOut, PositionOptionsOut
from app.schemas.base import CustomOutSchema


class User(BaseModel):
    username: str
    name: str
    mobile: Optional[str] = None
    email: Optional[EmailStr] = None
    gender: Optional[int] = 1
    is_superuser: Optional[bool] = False
    description: Optional[str] = None

    @classmethod
    @field_validator("mobile")
    def validate_mobile(cls, value: Optional[str]):
        return mobile_validator(value)


class CurrentUserUpdate(BaseModel):
    name: str
    mobile: Optional[str] = None
    email: Optional[EmailStr] = None
    gender: int
    avatar: Optional[str] = None


class CurrentUserPasswordChange(BaseModel):
    old_password: str
    new_password: str


class UserCreate(User):
    dept_id: int
    role_ids: List[int] = []
    position_ids: List[int] = []
    password: str


class UserUpdate(User):
    id: int
    dept_id: int
    role_ids: List[int] = []
    position_ids: List[int] = []
    password: Optional[str] = None
    available: Optional[bool]


class UserBatchSetAvailable(BaseModel):
    ids: List[int] = []


class UserPermissionSetting(BaseModel):
    user_ids: List[int] = []
    role_ids: List[int] = []


class UserOut(User, CustomOutSchema):
    model_config = ConfigDict(from_attributes=True)

    available: Optional[bool]


class UserSimpleOut(UserOut, CustomOutSchema):
    model_config = ConfigDict(from_attributes=True)

    avatar: Optional[str] = None
    dept_id: Optional[int] = None
    dept_name: Optional[str] = None
    roles: List[RoleOptionsOut] = []
    positions: List[PositionOptionsOut] = []
    last_login: Optional[DateTimeStr] = None


class UserPermissionOut(UserOut):
    model_config = ConfigDict(from_attributes=True)

    id: int
    avatar: Optional[str] = None
    dept_id: Optional[int] = None
    dept_name: Optional[str] = None
    roles: List[RolePermissionSimpleOut] = []
    positions: List[PositionOptionsOut] = []
    last_login: Optional[DateTimeStr] = None
