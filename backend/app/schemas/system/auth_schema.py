#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Union, Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.schemas.system import UserPermissionOut
from sqlalchemy.ext.asyncio import AsyncSession


class AuthUser(UserPermissionOut):
    ...


class Auth(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    user: Optional[AuthUser] = None
    check_data_scope: bool = False
    session: AsyncSession


class JWTPayload(BaseModel):
    sub: str
    is_refresh: bool
    exp: Union[datetime, int]


class RefreshTokenPayload(BaseModel):
    refresh_token: str


class JWTOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int


class CaptchaOut(BaseModel):
    key: str
    img_base: str
