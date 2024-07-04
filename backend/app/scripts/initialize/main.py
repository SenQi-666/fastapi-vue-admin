#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import TypeVar, List, Dict
from app.core.config import settings
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models.base import Model
from app.models import system
from pathlib import Path
import orjson


ModelType = TypeVar("ModelType", bound=Model)


class InitializeData:
    """
    初始化数据
    """

    SCRIPT_DIR: Path = Path.joinpath(settings.BASE_DIR, 'scripts', 'initialize')

    def __init__(self) -> None:
        self.engine = create_engine(self.__get_db_url(), echo=True, future=True)
        self.DBSession = sessionmaker(bind=self.engine)
        self.prepare_init_models = [
            system.DeptModel,
            system.UserModel,
            system.MenuModel,
            system.PositionModel,
            system.RoleModel,
            system.OperationLogModel,
            system.RoleDeptsModel,
            system.RoleMenusModel,
            system.UserPositionsModel,
            system.UserRolesModel
        ]

    def __get_db_url(self) -> str:
        scheme = settings.SQL_DB_URL.scheme.split('+')[0]
        new_db_url = settings.SQL_DB_URL.unicode_string().replace(settings.SQL_DB_URL.scheme, scheme)
        return new_db_url

    def __init_model(self) -> None:
        print("开始初始化数据库...")
        Model.metadata.create_all(
            self.engine,
            tables=[modal.__table__ for modal in self.prepare_init_models]
        )
        print("数据库初始化完成!")

    def __init_data(self) -> None:
        print("开始初始化数据...")

        for model in self.prepare_init_models:
            max_rows = self.__generate_data(model)
            self.__update_sequence(model, max_rows)

        print("数据初始化完成!")

    def __generate_data(self, model: ModelType) -> int:
        session = self.DBSession()

        table_name = model.__tablename__

        data = self.__get_data(table_name)
        objs = [model(**item) for item in data]
        session.add_all(objs)

        session.commit()
        session.close()
        print(f"{table_name} 表数据已生成!")

        return len(objs)

    def __get_data(self, filename: str) -> List[Dict]:
        try:
            json_path = Path.joinpath(self.SCRIPT_DIR, 'data', f'{filename}.json')
            with open(json_path, 'r', encoding='utf-8') as f:
                data = orjson.loads(f.read())
                return data

        except FileNotFoundError:
            return []

    def __update_sequence(self, model: ModelType, max_rows: int) -> None:
        table_name = model.__tablename__

        # 检查模型中是否有自增字段
        sequence_name = None
        for col in model.__table__.columns:
            if col.autoincrement is True:
                sequence_name = f"{table_name}_{col.name}_seq"
                break

        if not sequence_name:
            print(f"{table_name} 表无需设置自增序列值")
            return

        session = self.DBSession()

        # 更新序列最大值
        new_value = max_rows + 1
        session.execute(text(f"ALTER SEQUENCE {sequence_name} RESTART WITH {new_value}"))
        session.commit()
        print(f"{table_name} 表的自增序列值已更新!")

    def run(self) -> None:
        """
        执行初始化
        """
        if not settings.SQL_DB_ENABLE:
            return

        self.__init_model()
        self.__init_data()
