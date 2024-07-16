#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import FastAPI, applications
from app.core.config import settings
from app.utils.tools import import_module
from app.core.exceptions import (
    CustomException,
    CustomExceptionHandler,
    HTTPException,
    HttpExceptionHandler,
    RequestValidationError,
    ValidationExceptionHandler,
    SQLAlchemyError,
    SQLAlchemyExceptionHandler,
    AllExceptionHandler
)
from app.api import ApiRouter
from contextlib import asynccontextmanager
from app.core.database import redis_connect
from starlette.responses import HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    """
    自定义生命周期
    """

    await redis_connect(app, status=True)

    yield

    await redis_connect(app, status=False)


def register_middlewares(app: FastAPI) -> None:
    """
    注册中间件
    """
    for middleware in settings.MIDDLEWARE[::-1]:
        if not middleware:
            continue
        middleware = import_module(middleware)
        app.add_middleware(middleware)


def register_exceptions(app: FastAPI) -> None:
    """
    异常捕捉
    """
    app.add_exception_handler(CustomException, CustomExceptionHandler)
    app.add_exception_handler(HTTPException, HttpExceptionHandler)
    app.add_exception_handler(RequestValidationError, ValidationExceptionHandler)
    app.add_exception_handler(SQLAlchemyError, SQLAlchemyExceptionHandler)
    app.add_exception_handler(Exception, AllExceptionHandler)


def register_routers(app: FastAPI, prefix: str = "/") -> None:
    """
    注册根路由
    """
    app.include_router(ApiRouter, prefix=prefix)


def reset_api_docs() -> None:
    """
    修复Redoc API文档CDN无法访问的问题
    """

    def swagger_monkey_patch(*args, **kwargs):
        """
        修复Swagger API文档CDN无法访问的问题
        """
        return get_swagger_ui_html(
            *args, **kwargs,
            swagger_css_url="/static/swagger/swagger-ui/swagger-ui.css",
            swagger_js_url="/static/swagger/swagger-ui/swagger-ui-bundle.js",
            swagger_favicon_url="/static/swagger/favicon.png"
        )

    def redoc_monkey_patch(*args, **kwargs):
        return get_redoc_html(
            *args, **kwargs,
            redoc_js_url="/static/swagger/redoc/bundles/redoc.standalone.js",
            redoc_favicon_url="/static/swagger/favicon.png"
        )

    applications.get_swagger_ui_html = swagger_monkey_patch
    applications.get_redoc_html = redoc_monkey_patch
