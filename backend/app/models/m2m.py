#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.models.base import Model
from sqlalchemy import Column, BIGINT, ForeignKey


class RoleMenusModel(Model):
    __tablename__ = "system_role_menus"
    __table_args__ = ({'comment': '角色菜单关联表'})

    role_id = Column(
        BIGINT,
        ForeignKey("system_role.id", ondelete="CASCADE", onupdate="RESTRICT"),
        primary_key=True, comment="角色ID"
    )
    menu_id = Column(
        BIGINT,
        ForeignKey("system_menu.id", ondelete="CASCADE", onupdate="RESTRICT"),
        primary_key=True, comment="菜单ID"
    )


class RoleDeptsModel(Model):
    __tablename__ = "system_role_depts"
    __table_args__ = ({'comment': '角色数据权限部门关联表'})

    role_id = Column(
        BIGINT,
        ForeignKey("system_role.id", ondelete="CASCADE", onupdate="RESTRICT"),
        primary_key=True, comment="角色ID"
    )
    dept_id = Column(
        BIGINT,
        ForeignKey("system_dept.id", ondelete="CASCADE", onupdate="RESTRICT"),
        primary_key=True, comment="部门ID"
    )


class UserPositionsModel(Model):
    __tablename__ = "system_user_positions"
    __table_args__ = ({'comment': '用户岗位关联表'})

    user_id = Column(
        BIGINT,
        ForeignKey("system_user.id", ondelete="CASCADE", onupdate="RESTRICT"),
        primary_key=True, comment="用户ID"
    )
    position_id = Column(
        BIGINT,
        ForeignKey("system_position.id", ondelete="CASCADE", onupdate="RESTRICT"),
        primary_key=True, comment="岗位ID"
    )


class UserRolesModel(Model):
    __tablename__ = "system_user_roles"
    __table_args__ = ({'comment': '用户角色关联表'})

    user_id = Column(
        BIGINT,
        ForeignKey("system_user.id", ondelete="CASCADE", onupdate="RESTRICT"),
        primary_key=True, comment="用户ID"
    )
    role_id = Column(
        BIGINT,
        ForeignKey("system_role.id", ondelete="CASCADE", onupdate="RESTRICT"),
        primary_key=True, comment="角色ID"
    )
