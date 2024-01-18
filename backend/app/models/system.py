#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.models.base import Model, CustomMixin
from sqlalchemy.orm import relationship
from app.models.m2m import (
    RoleMenusModel,
    RoleDeptsModel,
    UserPositionsModel,
    UserRolesModel
)
from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    DateTime,
    Text,
    BIGINT,
    ForeignKey
)


class MenuModel(CustomMixin, Model):
    __tablename__ = "system_menu"
    __table_args__ = ({'comment': '菜单表'})

    name = Column(String(50), nullable=False, comment="菜单名称")
    type = Column(Integer, nullable=False, comment="菜单类型")
    icon = Column(String(50), nullable=False, default="", comment="图标")
    order = Column(Integer, nullable=False, default=1, comment="显示排序")
    permission = Column(String(50), nullable=False, default="", comment="权限标识")
    route_name = Column(String(50), nullable=True, comment="路由名称")
    route_path = Column(String(50), nullable=True, comment="路由路径")
    component_path = Column(String(50), nullable=True, comment="组件路径")
    available = Column(Boolean, nullable=False, default=True, comment="是否可用")
    cache = Column(Boolean, nullable=False, default=True, comment="是否缓存")
    hidden = Column(Boolean, nullable=False, default=False, comment="是否隐藏")
    parent_id = Column(
        BIGINT,
        ForeignKey("system_menu.id", ondelete="CASCADE", onupdate="RESTRICT"),
        nullable=True, index=True, comment="父级菜单ID"
    )
    parent_name = Column(String(50), nullable=True, comment="父级菜单名称")

    parent = relationship(
        "MenuModel",
        cascade='all, delete-orphan',
        primaryjoin="MenuModel.parent_id == MenuModel.id",
        uselist=False
    )


class DeptModel(CustomMixin, Model):
    __tablename__ = "system_dept"
    __table_args__ = ({'comment': '部门表'})

    name = Column(String(40), nullable=False, comment="部门名称")
    order = Column(Integer, nullable=False, default=1, comment="显示排序")
    available = Column(Boolean, nullable=False, default=True, comment="是否可用")
    parent_id = Column(
        BIGINT,
        ForeignKey("system_dept.id", ondelete="CASCADE", onupdate="RESTRICT"),
        nullable=True, index=True, comment="父级部门ID"
    )

    parent = relationship("DeptModel", cascade='all, delete-orphan', uselist=False)


class PositionModel(CustomMixin, Model):
    __tablename__ = "system_position"
    __table_args__ = ({'comment': '岗位表'})

    name = Column(String(40), nullable=False, comment="岗位名称")
    order = Column(Integer, nullable=False, default=1, comment="显示排序")
    available = Column(Boolean, default=True, nullable=False, comment="是否可用")

    users = relationship(
        "UserModel",
        secondary=UserPositionsModel.__tablename__,
        back_populates='positions',
        lazy="joined",
        uselist=True
    )


class RoleModel(CustomMixin, Model):
    __tablename__ = "system_role"
    __table_args__ = ({'comment': '角色表'})

    name = Column(String(40), nullable=False, comment="角色名称")
    order = Column(Integer, nullable=False, default=1, comment="显示排序")
    data_scope = Column(Integer, nullable=False, default=0, comment="数据权限")
    available = Column(Boolean, default=True, nullable=False, comment="是否可用")

    menus = relationship("MenuModel", secondary=RoleMenusModel.__tablename__, lazy="joined", uselist=True)
    depts = relationship("DeptModel", secondary=RoleDeptsModel.__tablename__, lazy="joined", uselist=True)


class UserModel(CustomMixin, Model):
    __tablename__ = "system_user"
    __table_args__ = ({'comment': '用户表'})

    username = Column(String(150), nullable=False, comment="用户名")
    password = Column(String(128), nullable=False, comment="密码")
    name = Column(String(40), nullable=False, comment="姓名")
    mobile = Column(String(20), nullable=True, comment="手机号")
    email = Column(String(255), nullable=True, comment="邮箱")
    gender = Column(Integer, default=1, nullable=False, comment="性别")
    avatar = Column(String(255), nullable=True, comment="头像")
    available = Column(Boolean, default=True, nullable=False, comment="是否可用")
    is_superuser = Column(Boolean, default=False, nullable=False, comment="是否超管")
    last_login = Column(DateTime, nullable=True, comment="最近登录时间")
    dept_id = Column(
        BIGINT,
        ForeignKey('system_dept.id', ondelete="SET NULL", onupdate="RESTRICT"),
        nullable=True, index=True, comment="部门ID"
    )

    dept = relationship('DeptModel', primaryjoin="UserModel.dept_id == DeptModel.id", uselist=False)
    roles = relationship("RoleModel", secondary=UserRolesModel.__tablename__, lazy="joined", uselist=True)
    positions = relationship("PositionModel", secondary=UserPositionsModel.__tablename__, lazy="joined", uselist=True)


class OperationLogModel(CustomMixin, Model):
    __tablename__ = "system_operation_log"
    __table_args__ = ({'comment': '操作日志表'})

    request_path = Column(String(255), nullable=True, comment="请求路径")
    request_method = Column(String(10), nullable=True, comment="请求方式")
    request_payload = Column(Text, nullable=True, comment="请求体")
    request_ip = Column(String(50), nullable=True, comment="请求IP地址")
    request_os = Column(String(64), nullable=True, comment="操作系统")
    request_browser = Column(String(64), nullable=True, comment="浏览器")
    response_code = Column(Integer, nullable=True, comment="响应状态码")
    response_json = Column(Text, nullable=True, comment="响应体")
