#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Dict, List
from app.crud.system import UserCRUD
from app.core.security import get_password_hash
from app.schemas.system import (
    Auth,
    UserCreate,
    UserUpdate,
    UserOut,
    UserSimpleOut,
    UserPermissionSetting
)


class UserService:
    """
    用户模块服务层
    """

    @classmethod
    async def get_detail_by_id(cls, id: int, auth: Auth) -> Dict:
        obj = await UserCRUD(auth).get_by_id(id)
        return UserSimpleOut.model_validate(obj).model_dump()

    @classmethod
    async def get_detail_by_username(cls, username, auth: Auth) -> UserSimpleOut:
        obj = await UserCRUD(auth).get_by_username(username)
        return UserSimpleOut.model_validate(obj)

    @classmethod
    async def get_current_user_info(cls, auth: Auth) -> Dict:
        return UserSimpleOut.model_validate(auth.user).model_dump()

    @classmethod
    async def get_user_list(cls, search: Dict, auth: Auth) -> List[Dict]:
        data = await UserCRUD(auth).get_user_list(search)
        data = [UserOut.model_validate(obj).model_dump() for obj in data]
        return data

    @classmethod
    async def create_user(cls, user_in: UserCreate, auth: Auth) -> Dict:
        user_in.password = get_password_hash(user_in.password)
        new_user = await UserCRUD(auth).create(
            obj_in=user_in.model_dump(exclude_unset=True, exclude={"role_ids", "position_ids"})
        )
        await UserCRUD(auth).set_user_roles([new_user.id], user_in.role_ids)
        await UserCRUD(auth).set_user_positions([new_user.id], user_in.position_ids)

        return UserOut.model_validate(new_user).model_dump()

    @classmethod
    async def update_user(cls, user_in: UserUpdate, auth: Auth) -> Dict:
        if user_in.password:
            user_in.password = get_password_hash(user_in.password)

        new_user = await UserCRUD(auth).update(id=user_in.id, obj_in=user_in)
        await UserCRUD(auth).set_user_roles([user_in.id], user_in.role_ids)
        await UserCRUD(auth).set_user_positions([user_in.id], user_in.position_ids)

        return UserOut.model_validate(new_user).model_dump()

    @classmethod
    async def delete_user(cls, id: int, auth: Auth) -> None:
        await UserCRUD(auth).delete(ids=[id])

    @classmethod
    async def set_user_available(cls, ids: List[int], available: bool, auth: Auth) -> None:
        await UserCRUD(auth).set_user_available(ids=ids, available=available)

    @classmethod
    async def set_user_permission(cls, permission_in: UserPermissionSetting, auth: Auth) -> None:
        await UserCRUD(auth).set_user_roles(permission_in.user_ids, permission_in.role_ids)
