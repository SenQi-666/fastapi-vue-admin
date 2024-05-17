#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from app.schemas.base import TimestampOutSchema


class Dept(BaseModel):
    name: str
    order: Optional[int] = 1
    parent_id: Optional[int] = None
    description: Optional[str] = None


class DeptCreate(Dept):
    ...


class DeptUpdate(Dept):
    id: int
    available: Optional[bool]


class DeptBatchSetAvailable(BaseModel):
    ids: List[int] = []


class DeptOut(Dept):
    model_config = ConfigDict(from_attributes=True)

    id: int
    available: Optional[bool]


class DeptSimpleOut(Dept, TimestampOutSchema):
    available: Optional[bool]


class DeptOptionsOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    parent_id: Optional[int] = None
