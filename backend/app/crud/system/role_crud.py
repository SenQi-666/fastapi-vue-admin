#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Dict, List, Sequence
from app.crud.base import CRUDBase
from app.models.system import RoleModel
from app.schemas.system import RoleCreate, RoleUpdate, Auth
from app.utils.tools import dict_to_search_sql
from app.crud.system import MenuCRUD, DeptCRUD
from sqlalchemy import update


class RoleCRUD(CRUDBase[RoleModel, RoleCreate, RoleUpdate]):
    """
    角色模块数据查询层
    """
    def __init__(self, auth: Auth) -> None:
        self.auth = auth
        super().__init__(model=RoleModel, auth=auth)

    async def get_by_id(self, id: int) -> RoleModel:
        obj = await self.get(id=id)
        return obj

    async def get_role_list(self, search: Dict = None, order: List[str] = None) -> Sequence[RoleModel]:
        sql_where = dict_to_search_sql(self.model, search) if search else None
        return await self.list(search=sql_where, order=order)

    async def set_role_menus(self, role_ids: List[int], menu_ids: List[int]) -> None:
        roles = await self.get_role_list(search={"id": ("in", role_ids)})
        menus = await MenuCRUD(self.auth).get_menu_list(search={"id": ("in", menu_ids)})

        for role in roles:
            role.menus.clear()
            for menu in menus:
                role.menus.append(menu)

        await self.session.flush()

    async def set_role_data_scope(self, role_ids: List[int], data_scope: int) -> None:
        roles = await self.get_role_list(search={"id": ("in", role_ids)})
        for role in roles:
            role.data_scope = data_scope

        await self.session.flush()

    async def set_role_depts(self, role_ids: List[int], dept_ids: List[int]) -> None:
        roles = await self.get_role_list(search={"id": ("in", role_ids)})
        depts = await DeptCRUD(self.auth).get_dept_list(search={"id": ("in", dept_ids)})

        for role in roles:
            role.depts.clear()
            for dept in depts:
                role.depts.append(dept)

        await self.session.flush()

    async def set_role_available(self, ids: List[int], available: bool) -> None:
        sql = update(self.model).where(self.model.id.in_(ids))
        sql = self.filter_permissions(sql).values(available=available)

        await self.session.execute(sql)
        await self.session.flush()
