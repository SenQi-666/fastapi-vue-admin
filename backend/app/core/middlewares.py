#!/usr/bin/env python
# -*- coding: utf-8 -*-

from starlette.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp
from starlette.requests import Request
from app.core.config import settings
from app.core.logger import logger
from starlette.middleware.base import (
    Response,
    BaseHTTPMiddleware,
    RequestResponseEndpoint
)
import time


class CustomCORSMiddleware(CORSMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super(CustomCORSMiddleware, self).__init__(app, **settings.get_cors_middleware_attributes)


class RequestLogMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super(RequestLogMiddleware, self).__init__(app)

    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start_time = time.time()
        response = await call_next(request)
        process_time = round(time.time() - start_time, 5)
        response.headers["X-Process-Time"] = str(process_time)
        self.write_request_log(request, response)

        return response

    @staticmethod
    def write_request_log(request: Request, response: Response) -> None:
        http_version = f"http/{request.scope['http_version']}"
        content_length = response.raw_headers[0][1].decode()
        process_time = response.headers["X-Process-Time"]
        content = f"'{request.method} {request.url} {http_version}' {response.status_code} {content_length} {process_time}"
        logger.info(content)
