#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Optional, List
from pydantic import BaseModel, model_validator, ConfigDict
from app.core.validator import menu_request_validator
from app.schemas.base import TimestampOutSchema


class Menu(BaseModel):
    name: str
    type: int
    icon: Optional[str] = ""
    order: Optional[int] = 1
    permission: Optional[str] = ""
    route_name: Optional[str] = None
    route_path: Optional[str] = None
    component_path: Optional[str] = None
    redirect: Optional[str] = None
    parent_id: Optional[int] = None
    parent_name: Optional[str] = None
    cache: Optional[bool] = True
    hidden: Optional[bool] = False
    description: Optional[str] = None

    @classmethod
    @model_validator(mode='after')
    def validate_fields(cls, data):
        return menu_request_validator(data)


class MenuCreate(Menu):
    ...


class MenuUpdate(Menu):
    id: int
    available: Optional[bool]


class MenuBatchSetAvailable(BaseModel):
    ids: List[int] = []


class MenuOut(TimestampOutSchema):
    name: str
    type: int
    icon: Optional[str] = ""
    order: Optional[int] = 1
    permission: Optional[str] = ""
    parent_id: Optional[int] = None
    available: Optional[bool]


class MenuSimpleOut(Menu, TimestampOutSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    available: Optional[bool]


class MenuOptionsOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    type: int
    permission: Optional[str] = ""
    parent_id: Optional[int] = None
    description: Optional[str] = None
    available: Optional[bool]
