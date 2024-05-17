#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import FastAPI
from app.core.config import settings
from starlette.staticfiles import StaticFiles
from app.core.init_app import (
    lifespan,
    register_middlewares,
    register_exceptions,
    register_routers,
    reset_swagger
)
import uvicorn, typer
from app.scripts.initialize import InitializeData


shell_app = typer.Typer()


def create_app() -> FastAPI:
    app = FastAPI(**settings.get_backend_app_attributes, lifespan=lifespan)
    # 注册异常处理器
    register_exceptions(app)
    # 挂载静态文件目录
    if settings.STATIC_ENABLE:
        app.mount(settings.STATIC_URL, app=StaticFiles(directory=settings.STATIC_ROOT))
    # 挂载临时文件目录
    if settings.TEMP_ENABLE:
        app.mount(settings.TEMP_URL, app=StaticFiles(directory=settings.TEMP_DIR))
    # 注册路由
    register_routers(app, prefix=settings.API_PREFIX)
    # 注册中间件
    register_middlewares(app)
    # 重设API文档
    reset_swagger(app)

    return app


@shell_app.command()
def run():
    uvicorn.run(
        app='main:create_app',
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        lifespan="on",
        factory=True
    )


@shell_app.command()
def init():
    """
    初始化数据
    """
    data = InitializeData()
    data.run()


if __name__ == '__main__':
    shell_app()
