#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Annotated, Optional, Union
from datetime import datetime
from pydantic import (
    AfterValidator,
    PlainSerializer,
    WithJsonSchema,
)
import re


def datetime_validator(value: Union[str, datetime]) -> Union[str, datetime, None]:
    """
    日期格式验证器
    :param value: 日期
    :return: 日期
    """
    pattern = "%Y-%m-%d %H:%M:%S"
    try:
        if isinstance(value, str):
            value = datetime.strptime(value, pattern)
        elif isinstance(value, datetime):
            value = value.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        raise ValueError("无效的日期数据")

    return value


# 实现自定义一个日期时间字符串的数据类型
DateTimeStr = Annotated[
    datetime,
    AfterValidator(lambda x: x.strftime("%Y-%m-%d %H:%M:%S")),
    PlainSerializer(lambda x: x, return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization')
]


def mobile_validator(value: Optional[str]) -> str:
    """
    手机号验证器
    :param value: 手机号
    :return: 手机号
    """
    if not value:
        return value

    if len(value) != 11 or not value.isdigit():
        raise ValueError("请输入正确手机号")

    regex = r'^1(3\d|4[4-9]|5[0-35-9]|6[67]|7[013-8]|8[0-9]|9[0-9])\d{8}$'

    if not re.match(regex, value):
        raise ValueError("请输入正确手机号")

    return value


def menu_request_validator(data):
    """
    菜单请求数据验证器
    :param data: 请求数据
    :return: 请求数据
    """
    if data.type not in [1, 2, 3]:
        raise ValueError("请选择正确菜单类型")
    elif data.type in [1, 2] and not data.route_name:
        raise ValueError("请输入路由名称")
    elif data.type in [1, 2] and not data.route_path:
        raise ValueError("请输入路由路径")
    elif data.type == 2 and not data.component_path:
        raise ValueError("请输入组件路径")
    return data


def role_permission_request_validator(data):
    """
    角色权限设置数据验证器
    :param data: 请求数据
    :return: 请求数据
    """
    if data.data_scope not in [1, 2, 3, 4, 5]:
        raise ValueError("请选择正确的数据权限")
    elif not data.role_ids:
        raise ValueError("请选择角色")
    return data
