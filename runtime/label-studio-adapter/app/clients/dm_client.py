import httpx
from typing import Optional
from app.core.config import settings
from app.core.logging import get_logger
from app.schemas.dm_service import DatasetResponse, PagedDatasetFileResponse

logger = get_logger(__name__)

class DMServiceClient:
    """数据管理服务客户端"""
    
    def __init__(self, base_url: str|None = None, timeout: float = 30.0):
        self.base_url = base_url or settings.dm_service_base_url
        self.timeout = timeout
        self.client = httpx.AsyncClient(
            base_url=self.base_url, 
            timeout=self.timeout
        )
        logger.info(f"初始化DM服务客户端，地址: {self.base_url}")
    
    async def get_dataset(self, dataset_id: str) -> Optional[DatasetResponse]:
        """获取数据集详情"""
        try:
            logger.info(f"获取数据集详情: {dataset_id}")
            response = await self.client.get(f"/data-management/datasets/{dataset_id}")
            response.raise_for_status()
            return DatasetResponse(**response.json())
        except httpx.HTTPError as e:
            logger.error(f"获取数据集 {dataset_id} 失败: {e}")
            return None
        except Exception as e:
            logger.error(f"获取数据集 {dataset_id} 时发生未知错误: {e}")
            return None
    
    async def get_dataset_files(
        self, 
        dataset_id: str, 
        page: int = 0, 
        size: int = 100,
        file_type: Optional[str] = None,
        status: Optional[str] = None
    ) -> Optional[PagedDatasetFileResponse]:
        """获取数据集文件列表"""
        try:
            logger.info(f"获取数据集文件列表: {dataset_id}, 页码: {page}, 大小: {size}")
            params: dict = {"page": page, "size": size}
            if file_type:
                params["fileType"] = file_type
            if status:
                params["status"] = status
                
            response = await self.client.get(
                f"/data-management/datasets/{dataset_id}/files",
                params=params
            )
            response.raise_for_status()
            return PagedDatasetFileResponse(**response.json())
        except httpx.HTTPError as e:
            logger.error(f"获取数据集 {dataset_id} 文件列表失败: {e}")
            return None
        except Exception as e:
            logger.error(f"获取数据集 {dataset_id} 文件列表时发生未知错误: {e}")
            return None
    
    async def download_file(self, dataset_id: str, file_id: str) -> Optional[bytes]:
        """下载文件内容"""
        try:
            logger.info(f"下载文件: 数据集={dataset_id}, 文件={file_id}")
            response = await self.client.get(
                f"/data-management/datasets/{dataset_id}/files/{file_id}/download"
            )
            response.raise_for_status()
            return response.content
        except httpx.HTTPError as e:
            logger.error(f"下载文件 {file_id} 失败: {e}")
            return None
        except Exception as e:
            logger.error(f"下载文件 {file_id} 时发生未知错误: {e}")
            return None
    
    async def get_file_download_url(self, dataset_id: str, file_id: str) -> str:
        """获取文件下载URL"""
        return f"{self.base_url}/data-management/datasets/{dataset_id}/files/{file_id}/download"
    
    async def close(self):
        """关闭客户端连接"""
        await self.client.aclose()
        logger.info("DM服务客户端连接已关闭")