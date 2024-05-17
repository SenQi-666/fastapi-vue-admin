#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Union, List, Dict, Optional
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, MySQLDsn, RedisDsn


class Settings(BaseSettings):
    # 项目根目录
    BASE_DIR: Path = Path(__file__).parent.parent

    # 调试模式 安全警告：不要在生产环境中打开调试运行！
    DEBUG: bool = True

    # 是否开启演示功能：取消所有POST,DELETE,PUT操作权限
    DEMO: bool = False
    # 演示功能白名单
    DEMO_WHITE_LIST_PATH: List[str] = [
        "/api/system/auth/login",
        "/api/system/auth/token/refresh"
    ]

    # 主机IP
    SERVER_HOST: str = "0.0.0.0"
    # 主机端口
    SERVER_PORT: int = 8080

    # 接口路由前缀
    API_PREFIX: str = "/api"

    # ================================================= #
    # ******************* API文档配置 ****************** #
    # ================================================= #
    # 文档标题
    TITLE: str = "Fastapi Vue Admin Application"
    # 版本号
    VERSION: str = "0.1.0"
    # 文档描述, 支持 Markdown 语法
    DESCRIPTION: Optional[str] = None
    # Swagger UI API文档路径
    DOCS_URL: Optional[str] = "/docs"
    # OpenAPI架构地址
    OPENAPI_URL: str = "/openapi.json"
    # ReDoc API文档路径
    REDOC_URL: Optional[str] = "/redoc"
    # OpenAPI路由前缀
    OPENAPI_PREFIX: str = ""

    # ================================================= #
    # ******************** 跨域配置 ******************** #
    # ================================================= #
    # 是否启用跨域
    CORS_ORIGIN_ENABLE: bool = True
    # 只允许访问的域名列表, * 代表所有
    ALLOW_ORIGINS: List[str] = ["*"]
    # 允许跨域的http方法, 例如 get、post、put 等
    ALLOW_METHODS: List[str] = ["*"]
    # 允许携带的headers, 可以用来鉴别来源等
    ALLOW_HEADERS: List[str] = ["*"]
    # 是否支持携带 cookie
    ALLOW_CREDENTIALS: bool = True

    # ================================================= #
    # ******************* 登录认证配置 ****************** #
    # ================================================= #
    # 安全的随机密钥, 该密钥将用于对 JWT 令牌进行签名
    SECRET_KEY: str = "vgb0tnl9d58+6n-6h-ea&u^1#s0ccp!794=krylxcjq75vzps$"
    # 用于设定 JWT 令牌签名算法
    ALGORITHM: str = "HS256"
    # access_token 过期时间
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    # refresh_token 过期时间
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    # ================================================= #
    # ***************** 静态文件目录配置 ***************** #
    # ================================================= #
    # 是否启用静态文件目录访问
    STATIC_ENABLE: bool = True
    # 路由访问
    STATIC_URL: str = "/static"
    # 静态文件目录名
    STATIC_DIR: str = "static"
    # 静态文件目录绝对路径
    STATIC_ROOT: Path = BASE_DIR.joinpath(STATIC_DIR)

    # ================================================= #
    # ***************** 临时文件目录配置 ***************** #
    # ================================================= #
    # 是否启用临时文件目录访问
    TEMP_ENABLE: bool = False
    # 路由访问
    TEMP_URL: str = "/temp"
    # 临时文件目录名
    TEMP_DIR: str = "temp"
    # 临时文件目录绝对路径
    TEMP_ROOT: Path = BASE_DIR.joinpath(TEMP_DIR)

    # ================================================= #
    # ******************** 数据库配置 ******************* #
    # ================================================= #
    SQL_DB_ENABLE: bool = True
    SQL_DB_URL: Union[PostgresDsn, MySQLDsn] = "postgresql+asyncpg://postgres:senqi1010@127.0.0.1:5432/fastapi_vue_admin"

    REDIS_ENABLE: bool = True
    REDIS_URL: RedisDsn = "redis://127.0.0.1:6379/0"

    # ================================================= #
    # ******************** 验证码配置 ******************* #
    # ================================================= #
    # 是否开启登录验证码功能
    CAPTCHA_ENABLE: bool = False
    # 验证码过期时间
    CAPTCHA_EXPIRE_SECONDS: int = 60

    # ================================================= #
    # ********************* 日志配置 ******************* #
    # ================================================= #
    # 是否开启保存每次请求日志到本地
    REQUEST_LOG_RECORD: bool = True
    # 是否开启每次操作日志记录到数据库
    OPERATION_LOG_RECORD: bool = True
    # 只记录包括的请求方式记录到数据库
    OPERATION_RECORD_METHOD: List[str] = ["POST", "PUT", "PATCH", "DELETE"]
    # 忽略的操作接口函数名称，列表中的函数名称不会被记录到操作日志中
    IGNORE_OPERATION_FUNCTION: List[str] = ["get_captcha_for_login"]

    # ================================================= #
    # ******************** 中间件配置 ******************* #
    # ================================================= #
    MIDDLEWARE: List[Optional[str]] = [
        "app.core.middlewares.CustomCORSMiddleware" if CORS_ORIGIN_ENABLE else None,
        "app.core.middlewares.RequestLogMiddleware" if REQUEST_LOG_RECORD else None,
        "app.core.middlewares.DemoEnvMiddleware" if DEMO else None,
    ]

    @property
    def get_backend_app_attributes(self) -> Dict[str, Union[str, bool, None]]:
        """
        设置 `FastAPI` 自定义属性
        """
        return {
            "debug": self.DEBUG,
            "title": self.TITLE,
            "version": self.VERSION,
            "description": self.DESCRIPTION,
            "docs_url": self.DOCS_URL,
            "openapi_url": self.OPENAPI_URL,
            "redoc_url": self.REDOC_URL,
            "openapi_prefix": self.OPENAPI_PREFIX
        }

    @property
    def get_cors_middleware_attributes(self) -> Dict[str, Union[List[str], bool]]:
        """
        设置 `CORSMiddleware` 自定义属性
        """
        return {
            "allow_origins": self.ALLOW_ORIGINS,
            "allow_methods": self.ALLOW_METHODS,
            "allow_headers": self.ALLOW_HEADERS,
            "allow_credentials": self.ALLOW_CREDENTIALS
        }


settings = Settings()
