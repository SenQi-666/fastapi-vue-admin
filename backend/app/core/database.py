#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.core.config import settings
from app.core.exceptions import CustomException
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)
import aioredis


def session_connect() -> async_sessionmaker:
    if not settings.SQL_DB_ENABLE:
        raise CustomException(msg="请先配置SQL数据库链接并启用", desc="请启用 app/core/config.py: SQL_DB_ENABLE")

    async_engine = create_async_engine(
        settings.SQL_DB_URL.unicode_string(),
        echo=False,
        echo_pool=False,
        pool_pre_ping=True,
        future=True
    )
    session_factory = async_sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=async_engine,
        expire_on_commit=False,
        class_=AsyncSession
    )
    return session_factory()


async def redis_connect(app: FastAPI, status: bool) -> None:
    if not settings.REDIS_ENABLE:
        raise CustomException(msg="请先配置Redis数据库链接并启用", desc="请启用 app/core/config.py: REDIS_ENABLE")

    if status:
        app.state.redis = aioredis.from_url(
            settings.REDIS_URL.unicode_string(),
            decode_responses=True,
            health_check_interval=20
        )
        print("Redis connected")
    else:
        print("Redis connection closed")
        await app.state.redis.close()

