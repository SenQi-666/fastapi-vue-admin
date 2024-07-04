#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Any, List, Dict, Sequence, Optional
import importlib, uuid, random
from pathlib import Path
from app.crud.base import ModelType
from app.models.base import Model
from sqlalchemy.sql.elements import ColumnElement
from fastapi import UploadFile
from app.core.config import settings
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


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


# 生成带有噪声和干扰的验证码图片
def generate_captcha(code) -> BytesIO:
    """
    生成带有噪声和干扰的验证码图片
    :return: 验证码图片流
    """
    # 创建一张随机颜色背景的图片
    background_color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
    width, height = 160, 60
    image = Image.new('RGB', (width, height), color=background_color)

    # 获取一个绘图对象
    draw = ImageDraw.Draw(image)

    # 字体设置（如果需要自定义字体，请替换下面的字体路径）
    font = ImageFont.truetype("./app/resources/gantians.otf", 42)

    # 计算验证码文本的总宽度
    total_text_width = 0
    for char in code:
        # 计算文本的宽度
        bbox = ImageDraw.Draw(Image.new('RGB', (1, 1))).textbbox((0, 0), char, font=font)
        text_width = bbox[2] - bbox[0]
        total_text_width += text_width

    # 计算每个字符的起始位置
    x_offset = (width - total_text_width) / 2
    # 计算文本的高度
    bbox = ImageDraw.Draw(Image.new('RGB', (1, 1))).textbbox((0, 0), code[0], font=font)
    text_height = bbox[3] - bbox[1]
    y_offset = (height - text_height) / 2 - draw.textbbox((0, 0), code[0], font=font)[1]

    # 绘制每个字符（单独的颜色和扭曲）
    for char in code:
        # 随机选择字体颜色
        text_color = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))

        # 计算字符位置并稍微扭曲
        bbox = ImageDraw.Draw(Image.new('RGB', (1, 1))).textbbox((0, 0), char, font=font)
        char_width = bbox[2] - bbox[0]
        char_x = x_offset + random.uniform(-3, 3)
        char_y = y_offset + random.uniform(-5, 5)

        # 绘制字符
        draw.text((char_x, char_y), char, font=font, fill=text_color)

        # 更新下一个字符的位置
        x_offset += char_width + random.uniform(2, 8)

    # 添加少量的圆圈干扰
    for _ in range(random.randint(2, 4)):
        # 随机位置和大小
        x = random.randint(0, width)
        y = random.randint(0, height)
        radius = random.randint(5, 10)
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), outline=text_color)

    # 添加少量的噪点
    for _ in range(random.randint(10, 20)):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        noise_size = random.randint(2, 4)
        noise_color = (random.randint(0, 50), random.randint(0, 50), random.randint(0, 50))
        draw.rectangle([x, y, x + noise_size, y + noise_size], fill=noise_color)

    # 返回验证码图片流
    stream = BytesIO()
    image.save(stream, format='PNG')

    return stream


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
