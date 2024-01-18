#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Dict, List
from app.crud.system import OperationLogCRUD
from app.schemas.system import (
    Auth,
    OperationLogCreate,
    OperationLogOut
)


class LogService:
    """
    日志模块服务层
    """

    @classmethod
    async def get_log_list(cls, search: Dict, auth: Auth) -> List[Dict]:
        data = await OperationLogCRUD(auth).get_log_list(search, order=["-created_at"])
        data = [OperationLogOut.model_validate(obj).model_dump() for obj in data]
        return data

    @classmethod
    async def create_log(cls, log_in: OperationLogCreate, auth: Auth) -> Dict:
        new_log = await OperationLogCRUD(auth).create(obj_in=log_in)
        return OperationLogOut.model_validate(new_log).model_dump()
