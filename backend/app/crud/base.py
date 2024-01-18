#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Generic, List, NewType, TypeVar, Sequence, Union, Dict, Any
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy.orm import selectinload
from pydantic import BaseModel
from sqlalchemy.engine import Result
from sqlalchemy import select, delete, Select, desc
from fastapi import status
from app.models.base import Model
from app.schemas.system import Auth
from app.core.exceptions import CustomException
from app.models.system import UserModel


Total = NewType("Total", int)
ModelType = TypeVar("ModelType", bound=Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    基础数据查询层
    """
    def __init__(self, model: ModelType, auth: Auth) -> None:
        self.model = model
        self.session = auth.session
        self.current_user = auth.user

    async def get(self, **kwargs) -> ModelType:
        columns = [getattr(self.model, key) == value for key, value in kwargs.items()]

        sql = select(self.model).where(*columns)
        if hasattr(self.model, "creator"):
            sql = sql.options(
                selectinload(self.model.creator)
            )

        sql = self.filter_permissions(sql)

        result: Result = await self.session.execute(sql)
        obj = result.scalars().unique().first()
        if not obj:
            raise CustomException(
                msg="该信息不存在",
                code=status.HTTP_404_NOT_FOUND,
                status_code=status.HTTP_404_NOT_FOUND
            )

        return obj

    async def list(self, search: List[ColumnElement] = None, order: List[str] = None) -> Sequence[ModelType]:
        if not search:
            search = []

        if not order:
            order = ["id"]

        sql = select(self.model).where(*search)
        if hasattr(self.model, "creator"):
            sql = sql.options(
                selectinload(self.model.creator)
            )

        sql = self.filter_permissions(sql).order_by(*self.get_order_columns(order))

        result: Result = await self.session.execute(sql)
        data = result.scalars().unique().all()

        return data

    async def create(self, obj_in: Union[CreateSchemaType, Dict]) -> ModelType:
        obj_dict = obj_in if isinstance(obj_in, Dict) else obj_in.model_dump()
        obj = self.model(**obj_dict)

        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)

        return obj

    async def update(self, id: int, obj_in: Union[UpdateSchemaType, Dict]) -> ModelType:
        obj_dict = obj_in if isinstance(obj_in, Dict) else obj_in.model_dump(exclude_unset=True, exclude={"id"})
        obj = await self.get(id=id)
        for key, value in obj_dict.items():
            setattr(obj, key, value)

        await self.session.flush()
        await self.session.refresh(obj)

        return obj

    async def delete(self, ids: List[int]) -> None:
        sql = delete(self.model).where(self.model.id.in_(ids))
        sql = self.filter_permissions(sql)

        await self.session.execute(sql)
        await self.session.flush()

    def get_order_columns(self, order: List[str]) -> List[ColumnElement]:
        columns = []
        for field in order:
            desc_order = False

            if field.startswith("-"):
                field = field[1:]
                desc_order = True

            column = getattr(self.model, field)
            if desc_order:
                column = desc(column)

            columns.append(column)

        return columns

    def filter_permissions(self, sql: Select[Any]) -> Select[Any]:
        if self.current_user is None:
            return sql

        if not hasattr(self.model, "creator"):
            return sql

        if self.current_user.is_superuser:
            return sql

        if not self.current_user.dept_id or not self.current_user.roles:
            return sql.where(self.model.creator_id == self.current_user.id)

        data_scopes = set()
        dept_ids = set()
        for role in self.current_user.roles:
            for dept in role.depts:
                dept_ids.add(dept.id)

        if 1 in data_scopes:
            return sql.where(self.model.creator_id == self.current_user.id)

        if 3 in data_scopes:
            dept_ids.add(self.current_user.dept_id)

        return sql.where(self.model.creator.has(UserModel.dept_id.in_(list(dept_ids))))
