#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from app.schemas.base import CustomOutSchema


class Position(BaseModel):
    name: str
    order: Optional[int] = 1
    description: Optional[str] = None


class PositionCreate(Position):
    ...


class PositionUpdate(Position):
    id: int
    available: Optional[bool]


class PositionBatchSetAvailable(BaseModel):
    ids: List[int] = []


class PositionOut(Position, CustomOutSchema):
    available: Optional[bool]


class PositionSimpleOut(PositionOut):
    ...


class PositionOptionsOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str] = None
    available: Optional[bool]
