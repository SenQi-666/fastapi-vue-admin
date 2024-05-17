#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Model
from app.models import system
from pathlib import Path
import orjson


class InitializeData:
    """
    初始化数据
    """

    SCRIPT_DIR: Path = Path.joinpath(settings.BASE_DIR, 'scripts', 'initialize')

    def __init__(self):
        self.engine = create_engine(self.__get_db_url(), echo=True, future=True)
        self.DBSession = sessionmaker(bind=self.engine)

    def __get_db_url(self):
        scheme = settings.SQL_DB_URL.scheme.split('+')[0]
        new_db_url = settings.SQL_DB_URL.unicode_string().replace(settings.SQL_DB_URL.scheme, scheme)
        return new_db_url

    def __init_model(self):
        print("开始初始化数据库...")
        Model.metadata.create_all(
            self.engine,
            tables=[
                system.DeptModel.__table__,
                system.UserModel.__table__,
                system.MenuModel.__table__,
                system.PositionModel.__table__,
                system.RoleModel.__table__,
                system.OperationLogModel.__table__,
                system.RoleDeptsModel.__table__,
                system.RoleMenusModel.__table__,
                system.UserPositionsModel.__table__,
                system.UserRolesModel.__table__
            ]
        )
        print("数据库初始化完成!")

    def __init_data(self):
        print("开始初始化数据...")
        self.__init_dept()
        self.__init_user()
        self.__init_menu()
        self.__init_position()
        self.__init_role()
        self.__init_role_depts()
        self.__init_role_menus()
        self.__init_user_positions()
        self.__init_user_roles()
        print("数据初始化完成!")

    def __generate_data(self, table_name: str, model: Model):
        session = self.DBSession()

        data = self.__get_data(table_name)
        objs = [model(**item) for item in data]
        session.add_all(objs)

        session.commit()
        session.close()
        print(f"{table_name} 表数据已生成!")

    def __get_data(self, filename: str):
        json_path = Path.joinpath(self.SCRIPT_DIR, 'data', f'{filename}.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            data = orjson.loads(f.read())
            return data

    def __init_dept(self):
        self.__generate_data("system_dept", system.DeptModel)

    def __init_menu(self):
        self.__generate_data("system_menu", system.MenuModel)

    def __init_position(self):
        self.__generate_data("system_position", system.PositionModel)

    def __init_role(self):
        self.__generate_data("system_role", system.RoleModel)

    def __init_role_depts(self):
        self.__generate_data("system_role_depts", system.RoleDeptsModel)

    def __init_role_menus(self):
        self.__generate_data("system_role_menus", system.RoleMenusModel)

    def __init_user(self):
        self.__generate_data("system_user", system.UserModel)

    def __init_user_positions(self):
        self.__generate_data("system_user_positions", system.UserPositionsModel)

    def __init_user_roles(self):
        self.__generate_data("system_user_roles", system.UserRolesModel)

    def run(self):
        """
        执行初始化
        """
        if not settings.SQL_DB_ENABLE:
            return

        self.__init_model()
        self.__init_data()
