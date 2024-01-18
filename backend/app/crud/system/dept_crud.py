#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Dict, List, Sequence
from app.crud.base import CRUDBase
from app.models.system import DeptModel
from app.schemas.system import DeptCreate, DeptUpdate, Auth
from app.utils.tools import dict_to_search_sql
from sqlalchemy import update


class DeptCRUD(CRUDBase[DeptModel, DeptCreate, DeptUpdate]):
    """
    部门模块数据查询层
    """
    def __init__(self, auth: Auth) -> None:
        super().__init__(model=DeptModel, auth=auth)

    async def get_by_id(self, id: int) -> DeptModel:
        obj = await self.get(id=id)
        return obj

    async def get_dept_list(self, search: Dict = None, order: List[str] = None) -> Sequence[DeptModel]:
        sql_where = dict_to_search_sql(self.model, search) if search else []
        return await self.list(search=sql_where, order=order)

    async def set_menu_available(self, ids: List[int], available: bool) -> None:
        sql = update(self.model).where(self.model.id.in_(ids)).values(available=available)
        await self.session.execute(sql)
        await self.session.flush()
