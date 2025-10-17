import httpx
from typing import Optional, Dict, Any, List
import json

from app.core.config import settings
from app.core.logging import get_logger
from app.schemas.label_studio import (
    LabelStudioProject, 
    LabelStudioCreateProjectRequest,
    LabelStudioCreateTaskRequest
)

logger = get_logger(__name__)

class LabelStudioClient:
    """Label Studio服务客户端
    
    使用 HTTP REST API 直接与 Label Studio 交互
    认证方式：使用 Authorization: Token {token} 头部进行认证
    """
    
    # 默认标注配置模板
    DEFAULT_LABEL_CONFIGS = {
        "image": """
        <View>
          <Image name="image" value="$image"/>
          <RectangleLabels name="label" toName="image">
            <Label value="Object" background="red"/>
          </RectangleLabels>
        </View>
        """,
        "text": """
        <View>
          <Text name="text" value="$text"/>
          <Choices name="sentiment" toName="text">
            <Choice value="positive"/>
            <Choice value="negative"/>
            <Choice value="neutral"/>
          </Choices>
        </View>
        """,
        "audio": """
        <View>
          <Audio name="audio" value="$audio"/>
          <AudioRegionLabels name="label" toName="audio">
            <Label value="Speech" background="red"/>
            <Label value="Noise" background="blue"/>
          </AudioRegionLabels>
        </View>
        """,
        "video": """
        <View>
          <Video name="video" value="$video"/>
          <VideoRegionLabels name="label" toName="video">
            <Label value="Action" background="red"/>
          </VideoRegionLabels>
        </View>
        """
    }
    
    def __init__(
        self, 
        base_url: Optional[str] = None, 
        token: Optional[str] = None,
        timeout: float = 30.0
    ):
        """初始化 Label Studio 客户端
        
        Args:
            base_url: Label Studio 服务地址
            token: API Token（使用 Authorization: Token {token} 头部）
            timeout: 请求超时时间（秒）
        """
        self.base_url = (base_url or settings.label_studio_base_url).rstrip("/")
        self.token = token or settings.label_studio_user_token
        self.timeout = timeout
        
        if not self.token:
            raise ValueError("必须提供 Label Studio API Token")
        
        # 初始化 HTTP 客户端
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            headers={
                "Authorization": f"Token {self.token}",
                "Content-Type": "application/json"
            }
        )
        
        logger.info(f"Label Studio 客户端已初始化: {self.base_url}")
    
    def get_label_config_by_type(self, data_type: str) -> str:
        """根据数据类型获取标注配置"""
        return self.DEFAULT_LABEL_CONFIGS.get(data_type.lower(), self.DEFAULT_LABEL_CONFIGS["image"])
    
    async def create_project(
        self, 
        title: str, 
        description: str = "", 
        label_config: Optional[str] = None,
        data_type: str = "image"
    ) -> Optional[Dict[str, Any]]:
        """创建Label Studio项目"""
        try:
            logger.info(f"创建Label Studio项目: {title}")
            
            if not label_config:
                label_config = self.get_label_config_by_type(data_type)
            
            project_data = {
                "title": title,
                "description": description,
                "label_config": label_config.strip()
            }
            
            response = await self.client.post("/api/projects", json=project_data)
            response.raise_for_status()
            
            project = response.json()
            project_id = project.get("id")
            
            if not project_id:
                raise Exception("Label Studio 返回的项目数据中没有 ID")
            
            logger.info(f"成功创建项目，ID: {project_id}")
            return project
        
        except httpx.HTTPStatusError as e:
            logger.error(f"创建项目失败 HTTP {e.response.status_code}: {e.response.text}")
            return None
        except Exception as e:
            logger.error(f"创建Label Studio项目时发生错误: {e}")
            return None
    
    async def import_tasks(
        self,
        project_id: int,
        tasks: List[Dict[str, Any]],
        commit_to_project: bool = True,
        return_task_ids: bool = True
    ) -> Optional[Dict[str, Any]]:
        """批量导入任务到Label Studio项目"""
        try:
            logger.info(f"开始向项目 {project_id} 导入 {len(tasks)} 个任务")
            
            response = await self.client.post(
                f"/api/projects/{project_id}/import",
                json=tasks,
                params={
                    "commit_to_project": str(commit_to_project).lower(),
                    "return_task_ids": str(return_task_ids).lower()
                }
            )
            response.raise_for_status()
            
            result = response.json()
            task_count = result.get("task_count", len(tasks))
            
            logger.info(f"成功导入任务: {task_count} 个")
            return result
            
        except httpx.HTTPStatusError as e:
            logger.error(f"导入任务失败 HTTP {e.response.status_code}: {e.response.text}")
            return None
        except Exception as e:
            logger.error(f"导入任务时发生错误: {e}")
            return None
    
    async def create_tasks_batch(
        self,
        project_id: str,
        tasks: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """批量创建任务的便利方法"""
        try:
            pid = int(project_id)
            return await self.import_tasks(pid, tasks)
        except ValueError as e:
            logger.error(f"项目ID格式错误: {project_id}, 错误: {e}")
            return None
        except Exception as e:
            logger.error(f"批量创建任务时发生错误: {e}")
            return None
    
    async def create_task(
        self,
        project_id: str,
        data: Dict[str, Any],
        meta: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """创建单个任务"""
        try:
            task = {"data": data}
            if meta:
                task["meta"] = meta
            
            return await self.create_tasks_batch(project_id, [task])
            
        except Exception as e:
            logger.error(f"创建单个任务时发生错误: {e}")
            return None
    
    async def get_project_tasks(
        self,
        project_id: str,
        page: int = 1,
        page_size: int = 100
    ) -> Optional[Dict[str, Any]]:
        """获取项目任务信息"""
        try:
            pid = int(project_id)
            
            logger.info(f"获取项目 {pid} 的任务信息")
            
            response = await self.client.get(
                f"/api/projects/{pid}/tasks",
                params={
                    "page": page,
                    "page_size": page_size
                }
            )
            response.raise_for_status()
            
            result = response.json()
            task_count = result.get("total", len(result.get("tasks", [])))
            
            return {
                "count": task_count,
                "page": page,
                "page_size": page_size,
                "project_id": pid,
                "tasks": result.get("tasks", [])
            }
            
        except httpx.HTTPStatusError as e:
            logger.error(f"获取项目任务失败 HTTP {e.response.status_code}: {e.response.text}")
            return None
        except Exception as e:
            logger.error(f"获取项目任务时发生错误: {e}")
            return None
    
    async def delete_task(
        self,
        task_id: int
    ) -> bool:
        """删除单个任务"""
        try:
            logger.info(f"删除任务: {task_id}")
            
            response = await self.client.delete(f"/api/tasks/{task_id}")
            response.raise_for_status()
            
            logger.info(f"成功删除任务: {task_id}")
            return True
            
        except httpx.HTTPStatusError as e:
            logger.error(f"删除任务 {task_id} 失败 HTTP {e.response.status_code}: {e.response.text}")
            return False
        except Exception as e:
            logger.error(f"删除任务 {task_id} 时发生错误: {e}")
            return False
    
    async def delete_tasks_batch(
        self,
        task_ids: List[int]
    ) -> Dict[str, int]:
        """批量删除任务"""
        try:
            logger.info(f"批量删除 {len(task_ids)} 个任务")
            
            successful_deletions = 0
            failed_deletions = 0
            
            for task_id in task_ids:
                if await self.delete_task(task_id):
                    successful_deletions += 1
                else:
                    failed_deletions += 1
            
            logger.info(f"批量删除完成: 成功 {successful_deletions} 个, 失败 {failed_deletions} 个")
            
            return {
                "successful": successful_deletions,
                "failed": failed_deletions,
                "total": len(task_ids)
            }
            
        except Exception as e:
            logger.error(f"批量删除任务时发生错误: {e}")
            return {
                "successful": 0,
                "failed": len(task_ids),
                "total": len(task_ids)
            }
    
    async def get_project(self, project_id: int) -> Optional[Dict[str, Any]]:
        """获取项目信息"""
        try:
            logger.info(f"获取项目信息: {project_id}")
            
            response = await self.client.get(f"/api/projects/{project_id}")
            response.raise_for_status()
            
            return response.json()
            
        except httpx.HTTPStatusError as e:
            logger.error(f"获取项目信息失败 HTTP {e.response.status_code}: {e.response.text}")
            return None
        except Exception as e:
            logger.error(f"获取项目信息时发生错误: {e}")
            return None
    
    async def delete_project(self, project_id: int) -> bool:
        """删除项目"""
        try:
            logger.info(f"删除项目: {project_id}")
            
            response = await self.client.delete(f"/api/projects/{project_id}")
            response.raise_for_status()
            
            logger.info(f"成功删除项目: {project_id}")
            return True
            
        except httpx.HTTPStatusError as e:
            logger.error(f"删除项目 {project_id} 失败 HTTP {e.response.status_code}: {e.response.text}")
            return False
        except Exception as e:
            logger.error(f"删除项目 {project_id} 时发生错误: {e}")
            return False

    async def close(self):
        """关闭客户端连接"""
        try:
            await self.client.aclose()
            logger.info("Label Studio客户端已关闭")
        except Exception as e:
            logger.error(f"关闭Label Studio客户端时发生错误: {e}")
