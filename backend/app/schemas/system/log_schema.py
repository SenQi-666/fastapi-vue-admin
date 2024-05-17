#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.schemas.base import CustomOutSchema


class OperationLog(BaseModel):
    request_path: Optional[str] = None
    request_method: Optional[str] = None
    request_payload: Optional[str] = None
    request_ip: Optional[str] = None
    request_os: Optional[str] = None
    request_browser: Optional[str] = None
    response_code: Optional[int] = None
    response_json: Optional[str] = None


class OperationLogCreate(OperationLog):
    ...


class OperationLogOut(OperationLog, CustomOutSchema):
    model_config = ConfigDict(from_attributes=True)
