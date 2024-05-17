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
from app.utils.tools import (
    get_parent_id_map,
    get_parent_recursion,
    get_child_id_map,
    get_child_recursion
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
    async def get_menu_list(cls, auth: Auth) -> List[Dict]:
        data = await MenuCRUD(auth).get_menu_list(order=["order"])
        data = [MenuSimpleOut.model_validate(obj).model_dump() for obj in data]
        return data

    @classmethod
    async def create_menu(cls, menu_in: MenuCreate, auth: Auth) -> Dict:
        if menu_in.parent_id:
            parent_menu = await MenuCRUD(auth).get_by_id(menu_in.parent_id)
            menu_in.parent_name = parent_menu.name
        new_menu = await MenuCRUD(auth).create(obj_in=menu_in)
        return MenuOut.model_validate(new_menu).model_dump()

    @classmethod
    async def update_menu(cls, menu_in: MenuUpdate, auth: Auth) -> Dict:
        if menu_in.parent_id:
            parent_menu = await MenuCRUD(auth).get_by_id(menu_in.parent_id)
            menu_in.parent_name = parent_menu.name
        new_menu = await MenuCRUD(auth).update(id=menu_in.id, obj_in=menu_in)
        if menu_in.available:
            await cls.enable_menu([menu_in.id], auth)
        else:
            await cls.disable_menu([menu_in.id], auth)

        return MenuOut.model_validate(new_menu).model_dump()

    @classmethod
    async def delete_menu(cls, id: int, auth: Auth) -> None:
        await MenuCRUD(auth).delete(ids=[id])

    @classmethod
    async def enable_menu(cls, ids: List[int], auth: Auth) -> None:
        data = await MenuCRUD(auth).get_menu_list()
        id_map = get_parent_id_map(model_list=data)

        enable_total_ids = []
        for menu_id in ids:
            enable_ids = get_parent_recursion(id=menu_id, id_map=id_map)
            enable_total_ids.extend(enable_ids)

        await MenuCRUD(auth).set_menu_available(ids=enable_total_ids, available=True)

    @classmethod
    async def disable_menu(cls, ids: List[int], auth: Auth) -> None:
        data = await MenuCRUD(auth).get_menu_list()
        id_map = get_child_id_map(model_list=data)

        disable_total_ids = []
        for menu_id in ids:
            disable_ids = get_child_recursion(id=menu_id, id_map=id_map)
            disable_total_ids.extend(disable_ids)

        await MenuCRUD(auth).set_menu_available(ids=disable_total_ids, available=False)

    @classmethod
    async def get_menu_options(cls, auth: Auth) -> List[Dict]:
        data = await MenuCRUD(auth).get_menu_list(search={"available": True}, order=["order"])
        data = [MenuOptionsOut.model_validate(obj).model_dump() for obj in data]
        return data
