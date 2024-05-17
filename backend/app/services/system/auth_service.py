#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import NewType, Dict, Union
import string, random, base64
from app.core.security import (
    CustomOAuth2PasswordRequestForm,
    verify_password,
    create_jwt_token,
    decode_jwt_token
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import CustomException
from aioredis import Redis
from captcha.image import ImageCaptcha
from io import BytesIO
from app.utils.tools import get_random_character
from datetime import timedelta
from app.core.config import settings
from app.crud.system import UserCRUD
from app.models.system import UserModel
from app.schemas.system import JWTPayload, JWTOut, Auth
from datetime import datetime
from fastapi import status


CaptchaKey = NewType('CaptchaKey', str)
CaptchaBase64 = NewType('CaptchaBase64', str)


class LoginService:
    """
    登录模块服务层
    """

    @classmethod
    async def authenticate_user(
            cls,
            login_form: CustomOAuth2PasswordRequestForm,
            session: AsyncSession,
            redis: Redis
    ) -> UserModel:
        if settings.CAPTCHA_ENABLE:
            await CaptchaService.check_captcha(key=login_form.captcha_key, captcha=login_form.captcha, redis=redis)

        auth = Auth(session=session)

        user = await UserCRUD(auth).get_by_username(login_form.username)
        if not verify_password(login_form.password, user.password):
            raise CustomException(
                msg="密码错误",
                code=status.HTTP_401_UNAUTHORIZED
            )

        if not user.available:
            raise CustomException(
                msg="用户已被停用",
                code=status.HTTP_403_FORBIDDEN
            )

        user = await UserCRUD(auth).update_last_login(user.id)
        return user

    @classmethod
    async def create_token(cls, username: str) -> JWTOut:
        expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_jwt_token(payload=JWTPayload(
            sub=username,
            is_refresh=False,
            exp=datetime.utcnow() + expires
        ))
        refresh_token = create_jwt_token(payload=JWTPayload(
            sub=username,
            is_refresh=True,
            exp=datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        ))
        return JWTOut(access_token=access_token, refresh_token=refresh_token, expires_in=expires.total_seconds())

    @classmethod
    async def refresh_token(cls, refresh_token: str) -> JWTOut:
        token_payload = decode_jwt_token(refresh_token)
        if not token_payload.is_refresh:
            raise CustomException(
                msg="非法凭证",
                code=status.HTTP_403_FORBIDDEN,
                status_code=status.HTTP_403_FORBIDDEN
            )

        username = token_payload.sub
        return await cls.create_token(username)


class CaptchaService:
    """
    验证码模块服务层
    """

    @classmethod
    async def get_captcha(cls, redis: Redis) -> Dict[str, Union[CaptchaKey, CaptchaBase64]]:
        if not settings.CAPTCHA_ENABLE:
            raise CustomException(msg="未开启验证码服务")

        total_strings = string.digits + string.ascii_lowercase
        random_strings = random.sample(list(total_strings), 4)
        captcha_string = "".join(random_strings)

        captcha: BytesIO = ImageCaptcha().generate(captcha_string)
        captcha_bytes = captcha.getvalue()
        captcha_base64 = base64.b64encode(captcha_bytes).decode()

        captcha_key = get_random_character()

        r_client = redis.client()
        await r_client.setex(
            f"captcha:{captcha_key}",
            timedelta(seconds=settings.CAPTCHA_EXPIRE_SECONDS),
            captcha_string
        )
        await r_client.close()

        return {
            "key": CaptchaKey(captcha_key),
            "img_base": CaptchaBase64(f"data:image/png;base64,{captcha_base64}")
        }

    @classmethod
    async def check_captcha(cls, key: str, captcha: str, redis: Redis) -> bool:
        if not captcha:
            raise CustomException(msg="验证码不能为空")

        r_client = redis.client()
        captcha_value = await r_client.get(f"captcha:{key}")
        if not captcha_value:
            raise CustomException(msg="验证码已过期")

        if captcha != str(captcha_value):
            raise CustomException(msg="验证码错误")

        return True
