#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Any, List, Dict, Sequence, Optional
import importlib, uuid
from app.crud.base import ModelType
from app.models.system import DeptModel
from sqlalchemy.sql.elements import ColumnElement


def import_module(module: str) -> Any:
    """
    导入模块
    :param module: 模块名称
    :return: 模块对象
    """
    module_path, module_class = module.rsplit(".", 1)
    module = importlib.import_module(module_path)
    cls = getattr(module, module_class)
    return cls


def dict_to_search_sql(model: ModelType, search: Dict) -> List[ColumnElement]:
    """
    用于搜索的参数字典转sql表达式数组
    :param model: 模型对象
    :param search: 搜索参数
    :return: sql表达式数组
    """
    sql_where = []

    for key, value in search.items():
        seq = None

        if isinstance(value, tuple):
            seq, value = value

        if value is None:
            continue

        if seq == "like":
            sql_where.append(getattr(model, key).like(f"%{value}%"))

        if seq == "in":
            sql_where.append(getattr(model, key).in_(value))

        if seq == "between":
            sql_where.append(getattr(model, key).between(*value))

        if seq is None:
            sql_where.append(getattr(model, key) == value)

    return sql_where


def get_random_character() -> str:
    """
    获取随机字符
    :return: 随机字符串
    """
    return uuid.uuid4().hex


def get_dept_enable_id_map(dept_list: Sequence[DeptModel]) -> Dict[int, int]:
    """
    递归启用部门ID的映射集
    :param dept_list: 部门模型数组
    :return: 映射集字典
    """
    data_map = {item.id: item.parent_id for item in dept_list}
    return data_map


def get_dept_enable_recursion(
        dept_id: int,
        dept_id_map: Dict[int, int],
        dept_ids: Optional[List[int]] = None
) -> List[int]:
    """
    递归获取启用的部门ID数组
    :param dept_id: 部门ID
    :param dept_id_map: 部门ID的映射集
    :param dept_ids: 部门ID数组
    :return: 启用的部门ID数组
    """
    if dept_ids is None:
        dept_ids = []

    dept_ids.append(dept_id)
    parent_id = dept_id_map.get(dept_id)
    if parent_id:
        get_dept_enable_recursion(parent_id, dept_id_map, dept_ids)

    return dept_ids


def get_dept_disable_id_map(dept_list: Sequence[DeptModel]) -> Dict[int, List[int]]:
    """
    递归禁用部门ID的映射集
    :param dept_list: 部门模型数组
    :return: 映射集字典
    """
    data_map = {}
    for dept in dept_list:
        data_map.setdefault(dept.id, [])
        if dept.parent_id:
            data_map.setdefault(dept.parent_id, []).append(dept.id)

    return data_map


def get_dept_disable_recursion(
        dept_id: int,
        dept_id_map: Dict[int, List[int]],
        dept_ids: Optional[List[int]] = None
) -> List[int]:
    """
    递归获取禁用的部门ID数组
    :param dept_id: 部门ID
    :param dept_id_map: 部门ID的映射集
    :param dept_ids: 部门ID数组
    :return: 禁用的部门ID数组
    """
    if dept_ids is None:
        dept_ids = []

    dept_ids.append(dept_id)
    child_ids = dept_id_map.get(dept_id, [])
    for child in child_ids:
        get_dept_disable_recursion(child, dept_id_map, dept_ids)

    return dept_ids
