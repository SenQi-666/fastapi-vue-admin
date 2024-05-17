#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Dict
from app.crud.system import DeptCRUD
from app.schemas.system import (
    Auth,
    DeptCreate,
    DeptUpdate,
    DeptOut,
    DeptSimpleOut,
    DeptOptionsOut
)
from app.utils.tools import (
    get_parent_id_map,
    get_parent_recursion,
    get_child_id_map,
    get_child_recursion
)


class DeptService:
    """
    部门模块服务层
    """

    @classmethod
    async def get_dept_detail(cls, id: int, auth: Auth) -> Dict:
        obj = await DeptCRUD(auth).get_by_id(id)
        return DeptSimpleOut.model_validate(obj).model_dump()

    @classmethod
    async def get_dept_list(cls, auth: Auth) -> List[Dict]:
        data = await DeptCRUD(auth).get_dept_list(order=["order"])
        data = [DeptOut.model_validate(obj).model_dump() for obj in data]
        return data

    @classmethod
    async def create_dept(cls, dept_in: DeptCreate, auth: Auth) -> Dict:
        new_dept = await DeptCRUD(auth).create(obj_in=dept_in)
        return DeptOut.model_validate(new_dept).model_dump()

    @classmethod
    async def update_dept(cls, dept_in: DeptUpdate, auth: Auth) -> Dict:
        new_dept = await DeptCRUD(auth).update(id=dept_in.id, obj_in=dept_in)
        if dept_in.available:
            await cls.enable_dept([new_dept.id], auth)
        else:
            await cls.disable_dept([new_dept.id], auth)

        return DeptOut.model_validate(new_dept).model_dump()

    @classmethod
    async def delete_dept(cls, id: int, auth: Auth) -> None:
        await DeptCRUD(auth).delete(ids=[id])

    @classmethod
    async def enable_dept(cls, ids: List[int], auth: Auth) -> None:
        data = await DeptCRUD(auth).get_dept_list()
        id_map = get_parent_id_map(model_list=data)

        enable_total_ids = []
        for dept_id in ids:
            enable_ids = get_parent_recursion(id=dept_id, id_map=id_map)
            enable_total_ids.extend(enable_ids)

        await DeptCRUD(auth).set_dept_available(ids=enable_total_ids, available=True)

    @classmethod
    async def disable_dept(cls, ids: List[int], auth: Auth) -> None:
        data = await DeptCRUD(auth).get_dept_list()
        id_map = get_child_id_map(model_list=data)

        disable_total_ids = []
        for dept_id in ids:
            disable_ids = get_child_recursion(id=dept_id, id_map=id_map)
            disable_total_ids.extend(disable_ids)

        await DeptCRUD(auth).set_dept_available(ids=disable_total_ids, available=False)

    @classmethod
    async def get_dept_options(cls, auth: Auth) -> List[Dict]:
        data = await DeptCRUD(auth).get_dept_list(search={"available": True}, order=["order"])
        data = [DeptOptionsOut.model_validate(obj).model_dump() for obj in data]
        return data
