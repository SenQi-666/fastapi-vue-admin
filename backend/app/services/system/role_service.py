#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Dict, List
from app.crud.system import RoleCRUD
from app.schemas.system import (
    Auth,
    RoleCreate,
    RoleUpdate,
    RoleOut,
    RoleSimpleOut,
    RoleOptionsOut,
    RolePermissionSetting
)


class RoleService:
    """
    角色模块服务层
    """

    @classmethod
    async def get_role_detail(cls, id: int, auth: Auth) -> Dict:
        obj = await RoleCRUD(auth).get_by_id(id)
        return RoleSimpleOut.model_validate(obj).model_dump()

    @classmethod
    async def get_role_list(cls, search: Dict, auth: Auth) -> List[Dict]:
        data = await RoleCRUD(auth).get_role_list(search, order=["order"])
        data = [RoleOut.model_validate(obj).model_dump() for obj in data]
        return data

    @classmethod
    async def create_role(cls, role_in: RoleCreate, auth: Auth) -> Dict:
        new_role = await RoleCRUD(auth).create(obj_in=role_in)
        return RoleOut.model_validate(new_role).model_dump()

    @classmethod
    async def update_role(cls, role_in: RoleUpdate, auth: Auth) -> Dict:
        new_menu = await RoleCRUD(auth).update(id=role_in.id, obj_in=role_in)
        return RoleOut.model_validate(new_menu).model_dump()

    @classmethod
    async def delete_role(cls, id: int, auth: Auth) -> None:
        await RoleCRUD(auth).delete(ids=[id])

    @classmethod
    async def set_role_permission(cls, permission_in: RolePermissionSetting, auth: Auth) -> None:
        await RoleCRUD(auth).set_role_menus(permission_in.role_ids, permission_in.menu_ids)
        await RoleCRUD(auth).set_role_data_scope(permission_in.role_ids, permission_in.data_scope)

        dept_ids = permission_in.dept_ids if permission_in.data_scope == 5 else []
        await RoleCRUD(auth).set_role_depts(permission_in.role_ids, dept_ids)

    @classmethod
    async def set_role_available(cls, ids: List[int], available: bool, auth: Auth) -> None:
        await RoleCRUD(auth).set_role_available(ids=ids, available=available)

    @classmethod
    async def get_role_options(cls, search: Dict, auth: Auth) -> List[Dict]:
        data = await RoleCRUD(auth).get_role_list(search)
        data = [RoleOptionsOut.model_validate(obj).model_dump() for obj in data]
        return data
