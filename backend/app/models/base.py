#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, BIGINT, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from datetime import datetime

Model = declarative_base(name='Model')


class TimestampMixin:
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")


class CustomMixin(TimestampMixin):
    """
    自定义公共 ORM 模型
    """

    id = Column(BIGINT, primary_key=True, autoincrement=True, unique=True, comment='主键ID', nullable=False)
    description = Column(Text, nullable=True, comment="备注")

    @declared_attr
    def creator_id(cls):
        return Column(
            BIGINT,
            ForeignKey("system_user.id", ondelete="SET NULL", onupdate="CASCADE"),
            nullable=True, index=True, comment="创建人"
        )

    @declared_attr
    def creator(cls):
        return relationship("UserModel", foreign_keys=cls.creator_id, lazy="selectin", uselist=False)
