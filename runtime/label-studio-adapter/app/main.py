from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .core.config import settings
from .core.logging import setup_logging, get_logger
from .db.database import init_db
from .clients import DMServiceClient, LabelStudioClient, set_clients
from .api import api_router

# 设置日志
setup_logging()
logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用程序生命周期管理"""
    
    # 启动时初始化
    logger.info("正在启动 Label Studio Adapter...")
    
    # 初始化客户端
    dm_client = DMServiceClient()
    
    # 初始化 Label Studio 客户端，使用 HTTP REST API + Token 认证
    ls_client = LabelStudioClient(
        base_url=settings.label_studio_base_url,
        token=settings.label_studio_user_token
    )
    
    # 设置全局客户端
    set_clients(dm_client, ls_client)
    
    # 初始化数据库
    await init_db()
    
    logger.info("Label Studio Adapter 启动完成")
    
    yield
    
    # 关闭时清理
    logger.info("正在关闭 Label Studio Adapter...")
    
    # 客户端清理会在客户端管理器中处理
    logger.info("Label Studio Adapter 已关闭")

# 创建FastAPI应用
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=settings.allowed_methods,
    allow_headers=settings.allowed_headers,
)

# 注册路由
app.include_router(api_router)

# 根路径重定向到文档
@app.get("/", include_in_schema=False)
async def root():
    """根路径，返回服务信息"""
    return {
        "message": f"{settings.app_name} 正在运行",
        "version": settings.app_version,
        "docs_url": "/docs",
        "dm_service_url": settings.dm_service_base_url,
        "label_studio_url": settings.label_studio_base_url
    }

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )