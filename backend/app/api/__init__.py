#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import APIRouter
from .system import SystemRouter


ApiRouter = APIRouter()

ApiRouter.include_router(SystemRouter, prefix="/system")
