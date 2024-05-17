#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import AsyncGenerator, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import session_connect
from fastapi import Request, Depends, status
from aioredis import Redis
from app.core.security import OAuth2Schema, decode_jwt_token
from app.core.exceptions import CustomException
from app.services.system import UserService
from app.schemas.system import Auth


async def session_getter() -> AsyncGenerator[AsyncSession, None]:
    async with session_connect() as session:
        async with session.begin():
            yield session


async def redis_getter(request: Request) -> Redis:
    return request.app.state.redis


async def get_current_user(
        request: Request,
        token: str = Depends(OAuth2Schema),
        session: AsyncSession = Depends(session_getter)
) -> Auth:
    token_payload = decode_jwt_token(token)
    if token_payload.is_refresh:
        raise CustomException(
            msg="非法凭证",
            code=status.HTTP_403_FORBIDDEN,
            status_code=status.HTTP_403_FORBIDDEN,
        )

    auth = Auth(session=session)

    username = token_payload.sub
    user = await UserService.get_detail_by_username(username, auth)
    if not user.available:
        raise CustomException(
            msg="用户已被停用",
            code=status.HTTP_403_FORBIDDEN,
        )

    request.scope["user_id"] = user.id
    user.roles = list(filter(lambda item: item.available, user.roles))
    user.positions = list(filter(lambda item: item.available, user.positions))
    auth.user = user

    return auth


class AuthPermission:

    def __init__(self, permissions: Optional[list[str]] = None, check_data_scope: bool = True) -> None:
        self.permissions = set(permissions) if permissions else None
        self.check_data_scope = check_data_scope

    async def __call__(
            self,
            request: Request,
            auth: Auth = Depends(get_current_user),
    ) -> Auth:

        auth.check_data_scope = self.check_data_scope

        is_superuser = auth.user.is_superuser
        if is_superuser:
            return auth

        if not self.permissions:
            return auth

        permissions = set()
        for role in auth.user.roles:
            for menu in role.menus:
                if not menu.permission:
                    continue
                permissions.add(menu.permission)

        if len(self.permissions) != len(self.permissions & permissions):
            raise CustomException(
                msg="无权限操作",
                code=status.HTTP_403_FORBIDDEN
            )

        return auth
