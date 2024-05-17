#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Dict, List
from fastapi import UploadFile
from app.crud.system import UserCRUD, MenuCRUD, DeptCRUD
from app.core.security import get_password_hash, verify_password
from app.core.exceptions import CustomException
from app.utils.tools import upload_image
from app.schemas.system import (
    Auth,
    UserCreate,
    UserUpdate,
    CurrentUserUpdate,
    CurrentUserPasswordChange,
    UserOut,
    UserSimpleOut,
    UserPermissionOut,
    MenuSimpleOut
)


class UserService:
    """
    用户模块服务层
    """

    @classmethod
    async def get_detail_by_id(cls, id: int, auth: Auth) -> Dict:
        obj = await UserCRUD(auth).get_by_id(id)
        dept = await DeptCRUD(auth).get(id=obj.dept_id)
        obj.dept_name = dept.name
        return UserSimpleOut.model_validate(obj).model_dump()

    @classmethod
    async def get_detail_by_username(cls, username, auth: Auth) -> UserPermissionOut:
        obj = await UserCRUD(auth).get_by_username(username)
        dept = await DeptCRUD(auth).get(id=obj.dept_id)
        obj.dept_name = dept.name
        return UserPermissionOut.model_validate(obj)

    @classmethod
    async def get_current_user_info(cls, auth: Auth) -> Dict:
        dept = await DeptCRUD(auth).get(id=auth.user.dept_id)
        user_obj = await UserCRUD(auth).get_by_id(auth.user.id)
        data = UserSimpleOut.model_validate(user_obj)
        data.dept_name = dept.name
        data = data.model_dump()

        if auth.user.is_superuser:
            menu_all = await MenuCRUD(auth).get_menu_list(search={'type': ('in', [1, 2]), 'available': True})
            menus = [MenuSimpleOut.model_validate(menu).model_dump() for menu in menu_all]
        else:
            menus = [
                MenuSimpleOut.model_validate(menu).model_dump()
                for role in auth.user.roles
                for menu in role.menus
                if menu.available
             ]

        data["menus"] = menus
        return data

    @classmethod
    async def get_user_list(cls, search: Dict, auth: Auth) -> List[Dict]:
        data = await UserCRUD(auth).get_user_list(search)
        new_data = []
        for obj in data:
            dept = await DeptCRUD(auth).get(id=obj.dept_id)
            obj.dept_name = dept.name
            new_data.append(UserSimpleOut.model_validate(obj).model_dump())

        return new_data

    @classmethod
    async def create_user(cls, user_in: UserCreate, auth: Auth) -> Dict:
        data = await UserCRUD(auth).get_user_list(search={'username': user_in.username})
        if data:
            raise CustomException(msg='已存在相同的账号')

        user_in.password = get_password_hash(user_in.password)
        new_user = await UserCRUD(auth).create(
            obj_in=user_in.model_dump(exclude_unset=True, exclude={"role_ids", "position_ids"})
        )
        await UserCRUD(auth).set_user_roles([new_user.id], user_in.role_ids)
        await UserCRUD(auth).set_user_positions([new_user.id], user_in.position_ids)

        return UserOut.model_validate(new_user).model_dump()

    @classmethod
    async def update_user(cls, user_in: UserUpdate, auth: Auth) -> Dict:
        user = await UserCRUD(auth).get_by_username(user_in.username)
        if user.id != user_in.id:
            raise CustomException(msg='已存在相同的用户名')

        if user_in.password:
            user_in.password = get_password_hash(user_in.password)

        new_user = await UserCRUD(auth).update(id=user_in.id, obj_in=user_in)
        await UserCRUD(auth).set_user_roles([user_in.id], user_in.role_ids)
        await UserCRUD(auth).set_user_positions([user_in.id], user_in.position_ids)

        return UserOut.model_validate(new_user).model_dump()

    @classmethod
    async def update_current_user_info(cls, data: CurrentUserUpdate, auth: Auth) -> Dict:
        new_user = await UserCRUD(auth).update(
            id=auth.user.id,
            obj_in=data.model_dump(exclude_unset=True, exclude={"id"})
        )
        return UserOut.model_validate(new_user).model_dump()

    @classmethod
    async def change_user_password(cls, data: CurrentUserPasswordChange, auth: Auth) -> Dict:
        if not data.old_password or not data.new_password:
            raise CustomException(msg='非法参数')

        user = await UserCRUD(auth).get_by_id(auth.user.id)
        if not verify_password(data.old_password, user.password):
            raise CustomException(msg='原密码输入错误')

        new_password_hash = get_password_hash(data.new_password)
        new_user = await UserCRUD(auth).change_password(user.id, new_password_hash)

        return UserOut.model_validate(new_user).model_dump()

    @classmethod
    async def delete_user(cls, id: int, auth: Auth) -> None:
        await UserCRUD(auth).delete(ids=[id])

    @classmethod
    async def set_user_available(cls, ids: List[int], available: bool, auth: Auth) -> None:
        await UserCRUD(auth).set_user_available(ids=ids, available=available)

    @classmethod
    async def upload_avatar(cls, file: UploadFile, auth: Auth) -> str:
        avatar = await upload_image(file, dirname='avatar')
        return avatar
