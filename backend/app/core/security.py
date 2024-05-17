#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Optional, Dict
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.security.utils import get_authorization_scheme_param
from fastapi import Form, Request, status
from passlib.context import CryptContext
from app.core.config import settings
from app.schemas.system import JWTPayload
from app.core.exceptions import CustomException
import jwt


class CustomOAuth2PasswordBearer(OAuth2PasswordBearer):
    def __init__(
            self,
            token_url: str,
            scheme_name: Optional[str] = None,
            scopes: Optional[Dict[str, str]] = None,
            description: Optional[str] = None,
            auto_error: bool = True
    ) -> None:
        super(CustomOAuth2PasswordBearer, self).__init__(token_url, scheme_name, scopes, description, auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization = request.headers.get("Authorization")
        scheme, token = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise CustomException(
                    msg="请登陆后再试",
                    code=status.HTTP_401_UNAUTHORIZED,
                    status_code=status.HTTP_401_UNAUTHORIZED
                )
            else:
                return None
        return token


class CustomOAuth2PasswordRequestForm(OAuth2PasswordRequestForm):
    """
    自定义OAuth2PasswordRequestForm类，增加验证码参数
    """
    def __init__(
            self,
            username: str = Form(),
            password: str = Form(),
            captcha_key: Optional[str] = Form(default=""),
            captcha: Optional[str] = Form(default="")
    ):
        super().__init__(username=username, password=password)
        self.captcha_key = captcha_key
        self.captcha = captcha


OAuth2Schema = CustomOAuth2PasswordBearer(token_url="/api/system/auth/login")

PwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return PwdContext.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return PwdContext.verify(plain_password, hashed_password)


def create_jwt_token(payload: JWTPayload) -> str:
    payload = payload.model_dump()
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_jwt_token(token: str) -> JWTPayload:
    if not token:
        raise CustomException(
            msg="请登陆后再试",
            code=status.HTTP_401_UNAUTHORIZED,
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise CustomException(
                msg="请登陆后再试",
                code=status.HTTP_401_UNAUTHORIZED,
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        return JWTPayload(**payload)

    except (jwt.InvalidSignatureError, jwt.DecodeError):
        raise CustomException(
            msg="无效认证，请重新登录",
            code=status.HTTP_403_FORBIDDEN,
            status_code=status.HTTP_403_FORBIDDEN
        )

    except jwt.ExpiredSignatureError:
        raise CustomException(
            msg="认证已过期，请重新登录",
            code=status.HTTP_401_UNAUTHORIZED,
            status_code=status.HTTP_401_UNAUTHORIZED
        )
