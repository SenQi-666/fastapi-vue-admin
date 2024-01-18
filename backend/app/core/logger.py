#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from loguru import logger
from app.core.config import settings

# 移除控制台输出
logger.remove(handler_id=None)

log_path = settings.BASE_DIR.joinpath("logs")
log_path.mkdir(parents=True, exist_ok=True)

log_path_info = log_path.joinpath(f"info_{time.strftime('%Y-%m-%d')}.log")
log_path_error = log_path.joinpath(f"error_{time.strftime('%Y-%m-%d')}.log")

info = logger.add(log_path_info, rotation="00:00", retention="3 days", enqueue=True, encoding="UTF-8", level="INFO")
error = logger.add(log_path_error, rotation="00:00", retention="3 days", enqueue=True, encoding="UTF-8", level="ERROR")

