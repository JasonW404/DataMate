from typing import Optional, List, Dict, Any, Tuple
from app.clients.dm_client import DMServiceClient
from app.clients.label_studio_client import LabelStudioClient
from app.services.dataset_mapping_service import DatasetMappingService
from app.schemas.dataset_mapping import SyncDatasetResponse
from app.core.logging import get_logger
from app.core.config import settings
from app.exceptions import NoDatasetInfoFoundError, DatasetMappingNotFoundError

logger = get_logger(__name__)

class SyncService:
    """数据同步服务"""
    
    def __init__(
        self, 
        dm_client: DMServiceClient, 
        ls_client: LabelStudioClient,
        mapping_service: DatasetMappingService
    ):
        self.dm_client = dm_client
        self.ls_client = ls_client
        self.mapping_service = mapping_service
    
    def determine_data_type(self, file_type: str) -> str:
        """根据文件类型确定数据类型"""
        file_type_lower = file_type.lower()
        
        if any(ext in file_type_lower for ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp']):
            return 'image'
        elif any(ext in file_type_lower for ext in ['mp3', 'wav', 'flac', 'aac', 'ogg']):
            return 'audio'
        elif any(ext in file_type_lower for ext in ['mp4', 'avi', 'mov', 'wmv', 'flv', 'webm']):
            return 'video'
        elif any(ext in file_type_lower for ext in ['txt', 'doc', 'docx', 'pdf']):
            return 'text'
        else:
            return 'image'  # 默认为图像类型
    
    async def get_existing_dm_file_mapping(self, project_id: str) -> Dict[str, int]:
        """
        获取Label Studio项目中已存在的DM文件ID到任务ID的映射
        
        Args:
            project_id: Label Studio项目ID
            
        Returns:
            dm_file_id到task_id的映射字典
        """
        try:
            logger.info(f"获取项目 {project_id} 中已存在的任务映射 (page_size={settings.ls_task_page_size})")
            dm_file_to_task_mapping = {}

            # 使用Label Studio SDK获取任务，尽量一次拉取足够多的记录，减少分页请求
            page_size = getattr(settings, 'ls_task_page_size', 1000)

            # The SDK returns an iterator; pass page_size to reduce number of HTTP requests
            tasks_iterator = self.ls_client.client.tasks.list(project=int(project_id), page_size=page_size)

            # Iterate defensively: Label Studio may return pagination errors if we request beyond available pages
            try:
                for task in tasks_iterator:
                    # 检查任务的meta字段中是否有dm_file_id
                    if hasattr(task, 'meta') and task.meta:
                        dm_file_id = task.meta.get('dm_file_id')
                        if dm_file_id:
                            dm_file_to_task_mapping[str(dm_file_id)] = task.id
            except Exception as inner_e:
                # 捕获Label Studio在分页时可能抛出的404/Invalid page等异常，记录并继续
                logger.warning(f"在遍历Label Studio任务时遇到分页/网络错误，已中断遍历: {inner_e}")

            logger.info(f"找到 {len(dm_file_to_task_mapping)} 个已存在的任务映射")
            return dm_file_to_task_mapping

        except Exception as e:
            logger.error(f"获取已存在任务时发生错误: {e}")
            return {}  # 发生错误时返回空字典，会同步所有文件
    
    async def sync_dataset_files(
        self, 
        mapping_id: str, 
        batch_size: int = 50
    ) -> SyncDatasetResponse:
        """同步数据集文件到Label Studio"""
        logger.info(f"开始根据映射关系同步数据集: {mapping_id}")
        
        # 获取映射关系
        mapping = await self.mapping_service.get_mapping_by_uuid(mapping_id)
        if not mapping:
            logger.error(f"未找到数据集映射: {mapping_id}")
            return SyncDatasetResponse(
                mapping_uuid="",
                status="error",
                synced_files=0,
                total_files=0,
                message=f"未找到数据集映射: {mapping_id}"
            )
        
        try:
            # 获取数据集信息
            dataset_info = await self.dm_client.get_dataset(mapping.source_dataset_uuid)
            if not dataset_info:
                raise NoDatasetInfoFoundError(mapping.source_dataset_uuid)
            
            synced_files = 0
            deleted_tasks = 0
            total_files = dataset_info.fileCount
            page = 0
            
            logger.info(f"数据集总文件数: {total_files}")
            
            # 获取Label Studio中已存在的DM文件ID到任务ID的映射
            existing_dm_file_mapping = await self.get_existing_dm_file_mapping(mapping.labelling_dataset_uuid)
            existing_dm_file_ids = set(existing_dm_file_mapping.keys())
            logger.info(f"Label Studio中已存在 {len(existing_dm_file_ids)} 个任务")
            
            # 收集DM中当前存在的所有文件ID
            current_dm_file_ids = set()
            
            # 分页获取并同步文件
            while True:
                files_response = await self.dm_client.get_dataset_files(
                    mapping.source_dataset_uuid, 
                    page=page, 
                    size=batch_size,
                    status="COMPLETED"  # 只同步已完成的文件
                )
                
                if not files_response or not files_response.content:
                    logger.info(f"第 {page + 1} 页没有更多文件")
                    break
                
                logger.info(f"处理第 {page + 1} 页，共 {len(files_response.content)} 个文件")
                
                # 筛选出新文件并批量创建任务
                tasks = []
                new_files_count = 0
                existing_files_count = 0
                
                for file_info in files_response.content:
                    # 记录当前DM中存在的文件ID
                    current_dm_file_ids.add(str(file_info.id))
                    
                    # 检查文件是否已存在
                    if str(file_info.id) in existing_dm_file_ids:
                        existing_files_count += 1
                        logger.debug(f"跳过已存在的文件: {file_info.originalName} (ID: {file_info.id})")
                        continue
                    
                    new_files_count += 1
                    
                    # 确定数据类型
                    data_type = self.determine_data_type(file_info.fileType)
                    
                    # 构造任务数据
                    task_data = {
                        "data": {
                            data_type: file_info.filePath.replace(
                                settings.dm_file_path_prefix,  # 从配置中获取DM存储文件夹前缀
                                settings.label_studio_file_path_prefix  # 从配置中获取Label Studio本地文件服务路径前缀
                            )
                        },
                        "meta": {
                            "file_size": file_info.size,
                            "file_type": file_info.fileType,
                            "dm_dataset_id": mapping.source_dataset_uuid,
                            "dm_file_id": file_info.id,
                            "original_name": file_info.originalName,
                        }
                    }
                    tasks.append(task_data)
                
                logger.info(f"第 {page + 1} 页: 新文件 {new_files_count} 个，已存在文件 {existing_files_count} 个")
                
                # 批量创建Label Studio任务
                if tasks:
                    batch_result = await self.ls_client.create_tasks_batch(
                        mapping.labelling_dataset_uuid,
                        tasks
                    )
                    
                    if batch_result:
                        synced_files += len(tasks)
                        logger.info(f"成功同步 {len(tasks)} 个文件")
                    else:
                        logger.warning(f"批量创建任务失败，尝试单个创建")
                        # 如果批量创建失败，尝试单个创建
                        for task_data in tasks:
                            task_result = await self.ls_client.create_task(
                                mapping.labelling_dataset_uuid,
                                task_data["data"],
                                task_data.get("meta")
                            )
                            if task_result:
                                synced_files += 1
                
                # 检查是否还有更多页面
                if page >= files_response.totalPages - 1:
                    break
                page += 1
            
            # 清理在DM中不存在但在Label Studio中存在的任务
            tasks_to_delete = []
            for dm_file_id, task_id in existing_dm_file_mapping.items():
                if dm_file_id not in current_dm_file_ids:
                    tasks_to_delete.append(task_id)
                    logger.debug(f"标记删除任务: {task_id} (DM文件ID: {dm_file_id})")
            
            if tasks_to_delete:
                logger.info(f"删除 {len(tasks_to_delete)} 个在DM中不存在的任务")
                delete_result = await self.ls_client.delete_tasks_batch(tasks_to_delete)
                deleted_tasks = delete_result.get("successful", 0)
                logger.info(f"成功删除 {deleted_tasks} 个任务")
            else:
                logger.info("没有需要删除的任务")
            
            # 更新映射的最后更新时间
            await self.mapping_service.update_last_updated_at(mapping.uuid)
            
            logger.info(f"同步完成: 总文件数={total_files}, 新增={synced_files}, 删除={deleted_tasks}")
            
            return SyncDatasetResponse(
                mapping_uuid=mapping.uuid,
                status="success",
                synced_files=synced_files,
                total_files=total_files,
                message=f"同步完成: 新增 {synced_files} 个文件, 删除 {deleted_tasks} 个任务"
            )
            
        except Exception as e:
            logger.error(f"同步数据集时发生错误: {e}")
            return SyncDatasetResponse(
                mapping_uuid=mapping.uuid,
                status="error",
                synced_files=0,
                total_files=0,
                message=f"同步失败: {str(e)}"
            )
    
    async def get_sync_status(
        self, 
        source_dataset_uuid: str
    ) -> Optional[Dict[str, Any]]:
        """获取同步状态"""
        mapping = await self.mapping_service.get_mapping_by_source_uuid(source_dataset_uuid)
        if not mapping:
            return None
        
        # 获取DM数据集信息
        dataset_info = await self.dm_client.get_dataset(source_dataset_uuid)
        
        # 获取Label Studio项目任务数量
        tasks_info = await self.ls_client.get_project_tasks(mapping.labelling_dataset_uuid)
        
        return {
            "mapping_uuid": mapping.uuid,
            "source_dataset_uuid": source_dataset_uuid,
            "labelling_dataset_uuid": mapping.labelling_dataset_uuid,
            "last_updated_at": mapping.last_updated_at,
            "dm_total_files": dataset_info.fileCount if dataset_info else 0,
            "ls_total_tasks": tasks_info.get("count", 0) if tasks_info else 0,
            "sync_ratio": (
                tasks_info.get("count", 0) / dataset_info.fileCount 
                if dataset_info and dataset_info.fileCount > 0 and tasks_info else 0
            )
        }