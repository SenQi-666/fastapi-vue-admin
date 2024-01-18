#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import Request, status
from app.utils.response import ErrorResponse
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.core.logger import logger


class CustomException(Exception):
    def __init__(
            self,
            msg: str,
            code: int = status.HTTP_400_BAD_REQUEST,
            status_code: int = status.HTTP_200_OK,
            desc: str = None
    ) -> None:
        self.msg = msg
        self.code = code
        self.status_code = status_code
        self.desc = desc


async def CustomExceptionHandler(request: Request, exc: CustomException) -> JSONResponse:
    """
    自定义异常处理器
    """
    print("请求地址", request.url.__str__(), exc.msg)
    logger.error(f"{exc.msg} {exc.desc}")
    return ErrorResponse(msg=exc.msg, code=exc.code, status_code=exc.status_code)


async def HttpExceptionHandler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    重写HTTPException异常处理器
    """
    print("请求地址", request.url.__str__(), exc.detail)
    logger.error(f"{exc.detail}")
    return ErrorResponse(msg=exc.detail, code=exc.status_code, status_code=exc.status_code)


async def ValidationExceptionHandler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    重写请求验证异常处理器
    """
    print("请求地址", request.url.__str__(), exc.errors())
    logger.error(f"{exc.errors()}")
    msg = exc.errors()[0].get("msg")
    return ErrorResponse(msg=msg, code=400, status_code=200)


async def SQLAlchemyExceptionHandler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """
    重写请求验证异常处理器
    """
    print("请求地址", request.url.__str__(), exc.__str__())
    logger.error(f"{exc.__str__()}")
    return ErrorResponse(msg="非法写入", code=400, status_code=200)


async def AllExceptionHandler(request: Request, exc: Exception) -> JSONResponse:
    """
    捕获全部异常
    """
    print("请求地址", request.url.__str__(), exc.__str__())
    logger.error(exc.__str__())
    return ErrorResponse(msg="接口异常", code=500, status_code=500)
