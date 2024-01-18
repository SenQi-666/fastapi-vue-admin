#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Dict, List
from app.crud.system import PositionCRUD
from app.schemas.system import (
    Auth,
    PositionCreate,
    PositionUpdate,
    PositionOut,
    PositionSimpleOut,
    PositionOptionsOut
)


class PositionService:
    """
    岗位模块服务层
    """

    @classmethod
    async def get_position_detail(cls, id: int, auth: Auth) -> Dict:
        obj = await PositionCRUD(auth).get_by_id(id)
        return PositionSimpleOut.model_validate(obj).model_dump()

    @classmethod
    async def get_position_list(cls, search: Dict, auth: Auth) -> List[Dict]:
        data = await PositionCRUD(auth).get_position_list(search, order=["order"])
        data = [PositionOut.model_validate(obj).model_dump() for obj in data]
        return data

    @classmethod
    async def create_position(cls, position_in: PositionCreate, auth: Auth) -> Dict:
        new_position = await PositionCRUD(auth).create(obj_in=position_in)
        return PositionOut.model_validate(new_position).model_dump()

    @classmethod
    async def update_position(cls, position_in: PositionUpdate, auth: Auth) -> Dict:
        new_position = await PositionCRUD(auth).update(id=position_in.id, obj_in=position_in)
        return PositionOut.model_validate(new_position).model_dump()

    @classmethod
    async def delete_position(cls, id: int, auth: Auth) -> None:
        await PositionCRUD(auth).delete(ids=[id])

    @classmethod
    async def set_position_available(cls, ids: List[int], available: bool, auth: Auth) -> None:
        await PositionCRUD(auth).set_position_available(ids=ids, available=available)

    @classmethod
    async def get_position_options(cls, search: Dict, auth: Auth) -> List[Dict]:
        data = await PositionCRUD(auth).get_position_list(search)
        data = [PositionOptionsOut.model_validate(obj).model_dump() for obj in data]
        return data
