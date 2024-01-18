#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Dict
from app.crud.system import MenuCRUD
from app.schemas.system import (
    Auth,
    MenuCreate,
    MenuUpdate,
    MenuOut,
    MenuSimpleOut,
    MenuOptionsOut
)


class MenuService:
    """
    菜单模块服务层
    """

    @classmethod
    async def get_menu_detail(cls, id: int, auth: Auth) -> Dict:
        obj = await MenuCRUD(auth).get_by_id(id)
        return MenuSimpleOut.model_validate(obj).model_dump()

    @classmethod
    async def get_menu_list(cls, search: Dict, auth: Auth) -> List[Dict]:
        data = await MenuCRUD(auth).get_menu_list(search, order=["order"])
        data = [MenuOut.model_validate(obj).model_dump() for obj in data]
        return data

    @classmethod
    async def create_menu(cls, menu_in: MenuCreate, auth: Auth) -> Dict:
        new_menu = await MenuCRUD(auth).create(obj_in=menu_in)
        return MenuOut.model_validate(new_menu).model_dump()

    @classmethod
    async def update_menu(cls, menu_in: MenuUpdate, auth: Auth) -> Dict:
        new_menu = await MenuCRUD(auth).update(id=menu_in.id, obj_in=menu_in)
        return MenuOut.model_validate(new_menu).model_dump()

    @classmethod
    async def delete_menu(cls, id: int, auth: Auth) -> None:
        await MenuCRUD(auth).delete(ids=[id])

    @classmethod
    async def set_menu_available(cls, ids: List[int], available: bool, auth: Auth) -> None:
        await MenuCRUD(auth).set_menu_available(ids=ids, available=available)

    @classmethod
    async def get_menu_options(cls, search: Dict, auth: Auth) -> List[Dict]:
        search["type"] = ("in", [1, 2])
        data = await MenuCRUD(auth).get_menu_list(search)
        data = [MenuOptionsOut.model_validate(obj).model_dump() for obj in data]
        return data
