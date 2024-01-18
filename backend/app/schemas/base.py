#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.core.validator import DateTimeStr


class TimestampOutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    created_at: DateTimeStr
    updated_at: DateTimeStr


class CreatorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class CustomOutSchema(TimestampOutSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    description: Optional[str] = None
    creator: Optional[CreatorOut]
