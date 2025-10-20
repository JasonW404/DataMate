from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.db.database import get_db
from app.services.dataset_mapping_service import DatasetMappingService
from app.clients import get_clients
from app.schemas.dataset_mapping import (
    DatasetMappingCreateRequest,
    DatasetMappingCreateResponse,
)
from app.core.logging import get_logger
from . import project_router

logger = get_logger(__name__)

@project_router.post("/create", response_model=DatasetMappingCreateResponse, status_code=201)
async def create_dataset_mapping(
    request: DatasetMappingCreateRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    创建数据集映射
    
    根据指定的DM程序中的数据集，创建Label Studio中的数据集，
    在数据库中记录这一关联关系，返回Label Studio数据集的ID
    
    注意：一个数据集可以创建多个标注项目
    """
    try:
        # 获取全局客户端实例
        dm_client_instance, ls_client_instance = get_clients()
        service = DatasetMappingService(db)
        
        logger.info(f"创建数据集映射请求: {request.source_dataset_id}")
        
        # 从DM服务获取数据集信息
        dataset_info = await dm_client_instance.get_dataset(request.source_dataset_id)
        if not dataset_info:
            raise HTTPException(
                status_code=404,
                detail=f"在DM服务中未找到数据集: {request.source_dataset_id}"
            )
        
        # 确定数据类型（基于数据集类型）
        data_type = "image"  # 默认值
        if dataset_info.type and dataset_info.type.code:
            type_code = dataset_info.type.code.lower()
            if "audio" in type_code:
                data_type = "audio"
            elif "video" in type_code:
                data_type = "video"
            elif "text" in type_code:
                data_type = "text"
        
        # 生成项目名称
        project_name = f"{dataset_info.name}"
        
        # 在Label Studio中创建项目
        project_data = await ls_client_instance.create_project(
            title=project_name,
            description=dataset_info.description or f"从DM数据集 {dataset_info.id} 导入",
            data_type=data_type
        )
        
        if not project_data:
            raise HTTPException(
                status_code=500,
                detail="Fail to create Label Studio project."
            )
        
        # 创建映射关系，包含项目名称
        mapping = await service.create_mapping(
            request, 
            str(project_data["id"]),
            project_name
        )
        
        logger.info(f"成功创建数据集映射: {mapping.uuid} -> S {mapping.source_dataset_id} <> L {mapping.labelling_project_id}")
        
        return DatasetMappingCreateResponse(
            mapping_uuid=mapping.uuid,
            labelling_project_id=mapping.labelling_project_id,
            labelling_project_name=mapping.labelling_project_name or project_name,
            message="数据集映射创建成功"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"创建数据集映射时发生错误: {e}")
        raise HTTPException(status_code=500, detail="内部服务器错误")