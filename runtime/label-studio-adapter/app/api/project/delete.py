from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.db.database import get_db
from app.services.dataset_mapping_service import DatasetMappingService
from app.clients import get_clients
from app.schemas.dataset_mapping import DeleteDatasetResponse
from app.core.logging import get_logger
from . import project_router

logger = get_logger(__name__)

@project_router.delete("/mappings", response_model=DeleteDatasetResponse)
async def delete_mapping(
    m: Optional[str] = Query(None, description="映射UUID"),
    proj: Optional[str] = Query(None, description="Label Studio项目ID"),
    db: AsyncSession = Depends(get_db)
):
    """
    删除映射关系和对应的 Label Studio 项目
    
    可以通过以下任一方式指定要删除的映射：
    - m: 映射UUID
    - proj: Label Studio项目ID
    - 两者都提供（优先使用 m）
    
    此操作会：
    1. 删除 Label Studio 中的项目
    2. 软删除数据库中的映射记录
    """
    try:
        # 至少需要提供一个参数
        if not m and not proj:
            raise HTTPException(
                status_code=400,
                detail="必须提供 m (映射UUID) 或 proj (项目ID) 参数"
            )
        
        # 获取全局客户端实例
        dm_client_instance, ls_client_instance = get_clients()
        service = DatasetMappingService(db)
        
        mapping = None
        
        # 优先使用 mapping_uuid 查询
        if m:
            logger.info(f"通过映射UUID删除: {m}")
            mapping = await service.get_mapping_by_uuid(m)
        # 如果没有提供 m，使用 proj 查询
        elif proj:
            logger.info(f"通过项目ID删除: {proj}")
            mapping = await service.get_mapping_by_labelling_project_id(proj)
        
        if not mapping:
            raise HTTPException(
                status_code=404,
                detail=f"未找到映射关系"
            )
        
        mapping_uuid = mapping.uuid
        labelling_project_id = mapping.labelling_project_id
        labelling_project_name = mapping.labelling_project_name
        
        logger.info(f"找到映射关系: {mapping_uuid}, Label Studio项目ID: {labelling_project_id}")
        
        # 1. 删除 Label Studio 项目
        try:
            delete_success = await ls_client_instance.delete_project(int(labelling_project_id))
            if delete_success:
                logger.info(f"成功删除 Label Studio 项目: {labelling_project_id}")
            else:
                logger.warning(f"删除 Label Studio 项目失败或项目不存在: {labelling_project_id}")
        except Exception as e:
            logger.error(f"删除 Label Studio 项目时发生错误: {e}")
            # 继续执行，即使 Label Studio 项目删除失败也要删除映射记录
        
        # 2. 软删除映射记录
        soft_delete_success = await service.soft_delete_mapping(mapping_uuid)
        
        if not soft_delete_success:
            raise HTTPException(
                status_code=500,
                detail="删除映射记录失败"
            )
        
        logger.info(f"成功删除映射关系: {mapping_uuid}")
        
        return DeleteDatasetResponse(
            mapping_uuid=mapping_uuid,
            status="success",
            message=f"成功删除映射关系和 Label Studio 项目 '{labelling_project_name}'"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除映射关系时发生错误: {e}")
        raise HTTPException(status_code=500, detail="内部服务器错误")
