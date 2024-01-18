#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Any, Tuple, List, Optional
from fastapi.responses import ORJSONResponse as Response
from fastapi import status
import math


class SuccessResponse(Response):
    """
    成功响应
    """
    def __init__(
            self,
            data: Optional[Any] = None,
            msg: Optional[str] = "success",
            code: int = status.HTTP_200_OK,
            status_code: int = status.HTTP_200_OK
    ) -> None:
        self.data = {
            "code": code,
            "data": data,
            "message": msg
        }
        super().__init__(content=self.data, status_code=status_code)


class ErrorResponse(Response):
    """
    失败响应
    """
    def __init__(
            self,
            msg: Optional[str] = None,
            code=status.HTTP_400_BAD_REQUEST,
            status_code=status.HTTP_200_OK
    ) -> None:
        self.data = {
            "code": code,
            "message": msg,
            "data": None
        }
        super().__init__(content=self.data, status_code=status_code)


class PaginationResponse(Response):
    """
    分页响应
    """
    def __init__(
            self,
            data: List[Any] = [],
            msg: Optional[str] = "success",
            page: int = 1,
            page_size: int = 10,
            code: int = status.HTTP_200_OK,
            status_code: int = status.HTTP_200_OK
    ) -> None:
        if page < 1 or page_size < 1:
            raise

        total, data = self.get_paginated_response(data, page, page_size)
        has_next = True if math.ceil(total / page_size) > page else False
        self.data = {
            "code": code,
            "total": total,
            "page": page,
            "page_size": page_size,
            "has_next": has_next,
            "data": data,
            "message": msg
        }
        super().__init__(content=self.data, status_code=status_code)

    @staticmethod
    def get_paginated_response(data, page, page_size) -> Tuple[int, List[Any]]:
        # 计算起始索引和结束索引
        start = (page - 1) * page_size
        end = page * page_size

        paginated_data = data[start:end]
        return len(data), paginated_data
