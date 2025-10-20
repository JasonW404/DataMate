"""
项目相关API路由模块
"""
from fastapi import APIRouter

# 创建项目路由器
project_router = APIRouter()

# 导入路由以确保它们被注册到 router 上
from . import create
from . import sync
from . import list
from . import delete