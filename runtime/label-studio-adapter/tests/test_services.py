import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.dataset_mapping_service import DatasetMappingService
from app.schemas.dataset_mapping import DatasetMappingCreateRequest

class TestDatasetMappingService:
    """测试数据集映射服务"""
    
    @pytest.mark.asyncio
    async def test_create_mapping(self, db_session):
        """测试创建映射"""
        service = DatasetMappingService(db_session)
        
        # 创建测试数据
        create_data = DatasetMappingCreateRequest(source_dataset_uuid="test-dataset-123")
        labelling_uuid = "label-project-456"
        
        # 执行创建
        result = await service.create_mapping(create_data, labelling_uuid)
        
        # 验证结果
        assert result.source_dataset_uuid == "test-dataset-123"
        assert result.labelling_dataset_uuid == "label-project-456"
        assert result.uuid is not None
        assert result.created_at is not None
        assert result.last_updated_at is not None
        assert result.deleted_at is None
    
    @pytest.mark.asyncio
    async def test_get_mapping_by_source_uuid(self, db_session):
        """测试根据源UUID查询映射"""
        service = DatasetMappingService(db_session)
        
        # 先创建一个映射
        create_data = DatasetMappingCreateRequest(source_dataset_uuid="test-dataset-789")
        created = await service.create_mapping(create_data, "label-project-999")
        
        # 查询映射
        result = await service.get_mapping_by_source_uuid("test-dataset-789")
        
        # 验证结果
        assert result is not None
        assert result.uuid == created.uuid
        assert result.source_dataset_uuid == "test-dataset-789"
    
    @pytest.mark.asyncio
    async def test_get_mapping_not_found(self, db_session):
        """测试查询不存在的映射"""
        service = DatasetMappingService(db_session)
        
        # 查询不存在的映射
        result = await service.get_mapping_by_source_uuid("non-existent-uuid")
        
        # 验证结果
        assert result is None
    
    @pytest.mark.asyncio
    async def test_soft_delete_mapping(self, db_session):
        """测试软删除映射"""
        service = DatasetMappingService(db_session)
        
        # 先创建一个映射
        create_data = DatasetMappingCreateRequest(source_dataset_uuid="test-delete-123")
        created = await service.create_mapping(create_data, "label-delete-456")
        
        # 软删除映射
        success = await service.soft_delete_mapping(created.uuid)
        assert success is True
        
        # 验证映射已被软删除（无法再查询到）
        result = await service.get_mapping_by_uuid(created.uuid)
        assert result is None