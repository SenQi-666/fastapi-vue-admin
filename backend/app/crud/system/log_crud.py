#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Dict, List, Sequence
from app.crud.base import CRUDBase
from app.models.system import OperationLogModel
from app.schemas.system import OperationLogCreate, Auth
from app.utils.tools import dict_to_search_sql


class OperationLogCRUD(CRUDBase[OperationLogModel, OperationLogCreate, None]):
    """
    日志模块数据查询层
    """
    def __init__(self, auth: Auth) -> None:
        super().__init__(model=OperationLogModel, auth=auth)

    async def get_log_list(self, search: Dict = None, order: List[str] = None) -> Sequence[OperationLogModel]:
        sql_where = dict_to_search_sql(self.model, search) if search else []
        return await self.list(search=sql_where, order=order)
