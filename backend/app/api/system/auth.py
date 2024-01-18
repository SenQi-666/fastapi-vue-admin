#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Union, Dict
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from app.core.router_class import OperationLogRoute
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import CustomOAuth2PasswordRequestForm
from app.core.dependencies import session_getter, redis_getter
from app.services.system import LoginService, CaptchaService
from app.utils.response import SuccessResponse
from app.schemas.system import JWTOut, RefreshTokenPayload, CaptchaOut
from app.core.config import settings
from aioredis import Redis


router = APIRouter(route_class=OperationLogRoute)


@router.post("/login", response_model=JWTOut, summary="登录", description="登录")
async def login_for_access_token(
        request: Request,
        login_form: CustomOAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(session_getter),
        redis: Redis = Depends(redis_getter),
) -> Union[JSONResponse, Dict]:
    user = await LoginService.authenticate_user(login_form, session, redis)
    login_token = await LoginService.create_token(user.username)

    if settings.DOCS_URL in request.headers.get("referer", ""):
        return login_token.model_dump()

    return SuccessResponse(login_token.model_dump(), msg="登录成功")


@router.post("/token/refresh", response_model=JWTOut, summary="刷新token", description="刷新token")
async def get_new_token(payload: RefreshTokenPayload) -> JSONResponse:
    new_token = await LoginService.refresh_token(payload.refresh_token)
    return SuccessResponse(new_token.model_dump(), msg="刷新成功")


@router.post("/captcha/get", response_model=CaptchaOut, summary="获取验证码", description="获取登录验证码")
async def get_captcha_for_login(redis: Redis = Depends(redis_getter)) -> JSONResponse:
    captcha = await CaptchaService.get_captcha(redis)
    return SuccessResponse(captcha, msg="获取成功")
