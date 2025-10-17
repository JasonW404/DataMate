from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from typing import Optional, List
from datetime import datetime
import uuid

from app.models.dataset_mapping import DatasetMapping
from app.schemas.dataset_mapping import (
    DatasetMappingCreateRequest, 
    DatasetMappingUpdateRequest, 
    DatasetMappingResponse
)
from app.core.logging import get_logger

logger = get_logger(__name__)

class DatasetMappingService:
    """数据集映射服务"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_mapping(
        self, 
        mapping_data: DatasetMappingCreateRequest, 
        labelling_project_id: str,
        labelling_project_name: str
    ) -> DatasetMappingResponse:
        """创建数据集映射"""
        logger.info(f"创建数据集映射: {mapping_data.source_dataset_id} -> {labelling_project_id}")
        
        db_mapping = DatasetMapping(
            uuid=str(uuid.uuid4()),
            source_dataset_id=mapping_data.source_dataset_id,
            labelling_project_id=labelling_project_id,
            labelling_project_name=labelling_project_name
        )
        
        self.db.add(db_mapping)
        await self.db.commit()
        await self.db.refresh(db_mapping)
        
        logger.info(f"成功创建映射: {db_mapping.uuid}")
        return DatasetMappingResponse.model_validate(db_mapping)
    
    async def get_mapping_by_source_uuid(
        self, 
        source_dataset_id: str
    ) -> Optional[DatasetMappingResponse]:
        """根据源数据集ID获取映射（返回第一个未删除的）"""
        logger.debug(f"查询源数据集映射: {source_dataset_id}")
        
        result = await self.db.execute(
            select(DatasetMapping).where(
                DatasetMapping.source_dataset_id == source_dataset_id,
                DatasetMapping.deleted_at.is_(None)
            )
        )
        mapping = result.scalar_one_or_none()
        
        if mapping:
            logger.debug(f"找到映射: {mapping.uuid}")
            return DatasetMappingResponse.model_validate(mapping)
        
        logger.debug(f"未找到源数据集映射: {source_dataset_id}")
        return None
    
    async def get_mappings_by_source_dataset_id(
        self, 
        source_dataset_id: str,
        include_deleted: bool = False
    ) -> List[DatasetMappingResponse]:
        """根据源数据集ID获取所有映射关系"""
        logger.debug(f"查询源数据集的所有映射: {source_dataset_id}")
        
        query = select(DatasetMapping).where(
            DatasetMapping.source_dataset_id == source_dataset_id
        )
        
        if not include_deleted:
            query = query.where(DatasetMapping.deleted_at.is_(None))
        
        result = await self.db.execute(
            query.order_by(DatasetMapping.created_at.desc())
        )
        mappings = result.scalars().all()
        
        logger.debug(f"找到 {len(mappings)} 个映射")
        return [DatasetMappingResponse.model_validate(mapping) for mapping in mappings]
    
    async def get_mapping_by_labelling_project_id(
        self, 
        labelling_project_id: str
    ) -> Optional[DatasetMappingResponse]:
        """根据Label Studio项目ID获取映射"""
        logger.debug(f"查询Label Studio项目映射: {labelling_project_id}")
        
        result = await self.db.execute(
            select(DatasetMapping).where(
                DatasetMapping.labelling_project_id == labelling_project_id,
                DatasetMapping.deleted_at.is_(None)
            )
        )
        mapping = result.scalar_one_or_none()
        
        if mapping:
            logger.debug(f"找到映射: {mapping.uuid}")
            return DatasetMappingResponse.model_validate(mapping)
        
        logger.debug(f"未找到Label Studio项目映射: {labelling_project_id}")
        return None
    
    async def get_mapping_by_uuid(self, mapping_uuid: str) -> Optional[DatasetMappingResponse]:
        """根据映射UUID获取映射"""
        logger.debug(f"查询映射: {mapping_uuid}")
        
        result = await self.db.execute(
            select(DatasetMapping).where(
                DatasetMapping.uuid == mapping_uuid,
                DatasetMapping.deleted_at.is_(None)
            )
        )
        mapping = result.scalar_one_or_none()
        
        if mapping:
            logger.debug(f"找到映射: {mapping.uuid}")
            return DatasetMappingResponse.model_validate(mapping)
        
        logger.debug(f"未找到映射: {mapping_uuid}")
        return None
    
    async def update_mapping(
        self, 
        mapping_uuid: str, 
        update_data: DatasetMappingUpdateRequest
    ) -> Optional[DatasetMappingResponse]:
        """更新映射信息"""
        logger.info(f"更新映射: {mapping_uuid}")
        
        mapping = await self.get_mapping_by_uuid(mapping_uuid)
        if not mapping:
            return None
        
        update_values = update_data.model_dump(exclude_unset=True)
        update_values["last_updated_at"] = datetime.utcnow()
        
        result = await self.db.execute(
            update(DatasetMapping)
            .where(DatasetMapping.uuid == mapping_uuid)
            .values(**update_values)
        )
        await self.db.commit()
        
        if result.rowcount > 0:
            return await self.get_mapping_by_uuid(mapping_uuid)
        return None
    
    async def update_last_updated_at(self, mapping_uuid: str) -> bool:
        """更新最后更新时间"""
        logger.debug(f"更新映射最后更新时间: {mapping_uuid}")
        
        result = await self.db.execute(
            update(DatasetMapping)
            .where(
                DatasetMapping.uuid == mapping_uuid,
                DatasetMapping.deleted_at.is_(None)
            )
            .values(last_updated_at=datetime.utcnow())
        )
        await self.db.commit()
        return result.rowcount > 0
    
    async def soft_delete_mapping(self, mapping_uuid: str) -> bool:
        """软删除映射"""
        logger.info(f"软删除映射: {mapping_uuid}")
        
        result = await self.db.execute(
            update(DatasetMapping)
            .where(
                DatasetMapping.uuid == mapping_uuid,
                DatasetMapping.deleted_at.is_(None)
            )
            .values(deleted_at=datetime.utcnow())
        )
        await self.db.commit()
        
        success = result.rowcount > 0
        if success:
            logger.info(f"成功软删除映射: {mapping_uuid}")
        else:
            logger.warning(f"映射不存在或已删除: {mapping_uuid}")
        
        return success
    
    async def get_all_mappings(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[DatasetMappingResponse]:
        """获取所有有效映射"""
        logger.debug(f"查询所有映射，跳过: {skip}, 限制: {limit}")
        
        result = await self.db.execute(
            select(DatasetMapping)
            .where(DatasetMapping.deleted_at.is_(None))
            .offset(skip)
            .limit(limit)
            .order_by(DatasetMapping.created_at.desc())
        )
        mappings = result.scalars().all()
        
        logger.debug(f"找到 {len(mappings)} 个映射")
        return [DatasetMappingResponse.model_validate(mapping) for mapping in mappings]
    
    async def count_mappings(self) -> int:
        """统计映射总数"""
        result = await self.db.execute(
            select(DatasetMapping)
            .where(DatasetMapping.deleted_at.is_(None))
        )
        mappings = result.scalars().all()
        return len(mappings)