#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Dict, List, Sequence
from app.crud.base import CRUDBase
from app.models.system import UserModel
from app.schemas.system import UserCreate, UserUpdate, Auth
from app.utils.tools import dict_to_search_sql
from datetime import datetime
from sqlalchemy import update
from app.crud.system import RoleCRUD, PositionCRUD


class UserCRUD(CRUDBase[UserModel, UserCreate, UserUpdate]):
    """
    用户模块数据查询层
    """
    def __init__(self, auth: Auth) -> None:
        self.auth = auth
        super().__init__(model=UserModel, auth=auth)

    async def get_by_id(self, id: int) -> UserModel:
        obj = await self.get(id=id)
        return obj

    async def get_by_username(self, username: str) -> UserModel:
        obj = await self.get(username=username)
        return obj

    async def get_user_list(self, search: Dict = None) -> Sequence[UserModel]:
        sql_where = dict_to_search_sql(self.model, search) if search else []
        return await self.list(search=sql_where)

    async def update_last_login(self, id: int) -> UserModel:
        obj = await self.update(id, obj_in={"last_login": datetime.now()})
        return obj

    async def set_user_available(self, ids: List[int], available: bool) -> None:
        sql = update(self.model).where(self.model.id.in_(ids)).values(available=available)
        await self.session.execute(sql)
        await self.session.flush()

    async def set_user_roles(self, user_ids: List[int], role_ids: List[int]) -> None:
        users = await self.get_user_list(search={"id": ("in", user_ids)})
        roles = await RoleCRUD(self.auth).get_role_list(search={"id": ("in", role_ids)})

        for user in users:
            user.roles.clear()
            for role in roles:
                user.roles.append(role)

        await self.session.flush()

    async def set_user_positions(self, user_ids: List[int], position_ids: List[int]) -> None:
        user_objs = await self.get_user_list(search={"id": ("in", user_ids)})
        position_objs = await PositionCRUD(self.auth).get_position_list(search={"id": ("in", position_ids)})

        for user_obj in user_objs:
            user_obj.positions.clear()
            for position_obj in position_objs:
                user_obj.positions.append(position_obj)

        await self.session.flush()

    async def change_password(self, id: int, password_hash: str):
        obj = await self.update(id, obj_in={"password": password_hash})
        return obj
