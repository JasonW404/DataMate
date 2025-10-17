from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_db
from app.services.dataset_mapping_service import DatasetMappingService
from app.schemas.dataset_mapping import DatasetMappingResponse
from app.core.logging import get_logger
from . import project_router

logger = get_logger(__name__)

@project_router.get("/mappings/list", response_model=List[DatasetMappingResponse])
async def list_mappings(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回的最大记录数"),
    db: AsyncSession = Depends(get_db)
):
    """
    查询所有映射关系
    
    返回所有有效的数据集映射关系（未被软删除的）
    """
    try:
        service = DatasetMappingService(db)
        
        logger.info(f"查询映射关系列表，skip={skip}, limit={limit}")
        
        mappings = await service.get_all_mappings(skip=skip, limit=limit)
        
        logger.info(f"成功查询到 {len(mappings)} 个映射关系")
        
        return mappings
        
    except Exception as e:
        logger.error(f"查询映射关系列表时发生错误: {e}")
        raise HTTPException(status_code=500, detail="内部服务器错误")


@project_router.get("/mappings/{mapping_uuid}", response_model=DatasetMappingResponse)
async def get_mapping(
    mapping_uuid: str,
    db: AsyncSession = Depends(get_db)
):
    """
    根据 UUID 查询单个映射关系
    """
    try:
        service = DatasetMappingService(db)
        
        logger.info(f"查询映射关系: {mapping_uuid}")
        
        mapping = await service.get_mapping_by_uuid(mapping_uuid)
        
        if not mapping:
            raise HTTPException(
                status_code=404,
                detail=f"未找到映射关系: {mapping_uuid}"
            )
        
        logger.info(f"成功查询到映射关系: {mapping.uuid}")
        
        return mapping
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"查询映射关系时发生错误: {e}")
        raise HTTPException(status_code=500, detail="内部服务器错误")


@project_router.get("/mappings/by-source/{source_dataset_id}", response_model=List[DatasetMappingResponse])
async def get_mappings_by_source(
    source_dataset_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    根据源数据集 ID 查询所有映射关系
    
    返回该数据集创建的所有标注项目（包括已删除的）
    """
    try:
        service = DatasetMappingService(db)
        
        logger.info(f"根据源数据集ID查询映射关系: {source_dataset_id}")
        
        mappings = await service.get_mappings_by_source_dataset_id(source_dataset_id)
        
        logger.info(f"成功查询到 {len(mappings)} 个映射关系")
        
        return mappings
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"查询映射关系时发生错误: {e}")
        raise HTTPException(status_code=500, detail="内部服务器错误")
