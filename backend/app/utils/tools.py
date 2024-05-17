#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Any, List, Dict, Sequence, Optional
import importlib, uuid
from pathlib import Path
from app.crud.base import ModelType
from app.models.base import Model
from sqlalchemy.sql.elements import ColumnElement
from fastapi import UploadFile
from app.core.config import settings


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
            start, end = value
            if not start or not end:
                continue
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


def get_parent_id_map(model_list: Sequence[Model]) -> Dict[int, int]:
    """
    获取父级ID的映射集
    :param model_list: 模型数组
    :return: 映射集字典
    """
    data_map = {item.id: item.parent_id for item in model_list}
    return data_map


def get_parent_recursion(
        id: int,
        id_map: Dict[int, int],
        ids: Optional[List[int]] = None
) -> List[int]:
    """
    递归获取某ID的所有父级的ID数组
    :param id: ID
    :param id_map: ID的映射集
    :param ids: ID数组
    :return: 所有父级的ID数组
    """
    if ids is None:
        ids = []

    ids.append(id)
    parent_id = id_map.get(id)
    if parent_id:
        get_parent_recursion(parent_id, id_map, ids)

    return ids


def get_child_id_map(model_list: Sequence[Model]) -> Dict[int, List[int]]:
    """
    获取子级ID的映射集
    :param model_list: 模型数组
    :return: 映射集字典
    """
    data_map = {}
    for model in model_list:
        data_map.setdefault(model.id, [])
        if model.parent_id:
            data_map.setdefault(model.parent_id, []).append(model.id)

    return data_map


def get_child_recursion(
        id: int,
        id_map: Dict[int, List[int]],
        ids: Optional[List[int]] = None
) -> List[int]:
    """
    递归获取某ID的所有子级的ID数组
    :param id: ID
    :param id_map: ID的映射集
    :param ids: ID数组
    :return: 所有子级的ID数组
    """
    if ids is None:
        ids = []

    ids.append(id)
    child_ids = id_map.get(id, [])
    for child in child_ids:
        get_child_recursion(child, id_map, ids)

    return ids


async def upload_image(file: UploadFile, dirname: str) -> Optional[str]:
    """
    图片上传
    :param file: 文件对象
    :param dirname: 文件目录
    :return: 图片链接
    """
    if 'image' not in file.content_type:
        return

    image_type = file.content_type.split('/')[1]
    image_name = f'{uuid.uuid4().hex}.{image_type}'

    image_path = Path(f'{settings.STATIC_ROOT}/{dirname}')
    if not image_path.exists():
        image_path.mkdir(parents=True, exist_ok=True)

    image_path = f'{settings.STATIC_ROOT}/{dirname}/{image_name}'
    with open(image_path, 'wb') as f:
        f.write(await file.read())

    image_url = f'{settings.STATIC_DIR}/{dirname}/{image_name}'
    return image_url
