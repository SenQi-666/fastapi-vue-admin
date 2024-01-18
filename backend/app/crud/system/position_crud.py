
from typing import Dict, List, Sequence
from app.crud.base import CRUDBase
from app.models.system import PositionModel
from app.schemas.system import PositionCreate, PositionUpdate, Auth
from app.utils.tools import dict_to_search_sql
from sqlalchemy import update


class PositionCRUD(CRUDBase[PositionModel, PositionCreate, PositionUpdate]):
    """
    岗位模块数据查询层
    """
    def __init__(self, auth: Auth) -> None:
        super().__init__(model=PositionModel, auth=auth)

    async def get_by_id(self, id: int) -> PositionModel:
        obj = await self.get(id=id)
        return obj

    async def get_position_list(self, search: Dict = None, order: List[str] = None) -> Sequence[PositionModel]:
        sql_where = dict_to_search_sql(self.model, search) if search else None
        return await self.list(search=sql_where, order=order)

    async def set_position_available(self, ids: List[int], available: bool) -> None:
        sql = update(self.model).where(self.model.id.in_(ids)).values(available=available)
        await self.session.execute(sql)
        await self.session.flush()
