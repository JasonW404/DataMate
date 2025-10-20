from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()

@router.get("/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "service": "Label Studio Adapter",
        "version": settings.app_version
    }

@router.get("/config")
async def get_config():
    """获取配置信息"""
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "dm_service_url": settings.dm_service_base_url,
        "label_studio_url": settings.label_studio_base_url,
        "debug": settings.debug
    }