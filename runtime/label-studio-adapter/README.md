# Label Studio Adapter

一个用于集成数据管理系统(DM)与Label Studio的适配器服务。

## 功能特性

1. **创建数据集映射**: 根据指定的DM程序中的数据集，创建Label Studio中的数据集，并记录映射关系
2. **同步数据集内容**: 将DM程序数据集中的文件同步到Label Studio数据集中
3. **删除数据集映射**: 根据指定的UUID，删除Label Studio中对应的数据集

## 技术栈

- **框架**: FastAPI
- **数据库**: PostgreSQL + SQLAlchemy (异步)
- **HTTP客户端**: httpx
- **数据验证**: Pydantic

## 环境配置

通过环境变量配置服务：

```bash
# Label Studio服务地址
LABEL_STUDIO_BASE_URL=http://label-studio:8080

# Label Studio 认证配置 (支持两种方式)
# 方式1: Legacy Token (推荐，默认使用)
LABEL_STUDIO_USER_TOKEN=your-legacy-token-here
# 方式2: JWT Token (备用)
LABEL_STUDIO_API_KEY=your-jwt-refresh-token-here

# 数据管理服务地址
DM_SERVICE_BASE_URL=http://data-engine

# 数据库连接
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/labelstudio_adapter

# API配置
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
```

### Label Studio 认证方式

Adapter 支持两种 Label Studio API 认证方式：

1. **Legacy Token（推荐，默认）**: 使用 `Authorization: Token {token}` 头部认证
   - 配置简单，适合开发环境
   - Token 不会过期（除非手动撤销）
   - 在 `.env` 中设置 `LABEL_STUDIO_USER_TOKEN`

2. **JWT Token（备用）**: 使用 JWT refresh token 认证
   - 安全性更高，适合生产环境
   - Token 有过期时间
   - 在 `.env` 中设置 `LABEL_STUDIO_API_KEY`

详细说明请参考 [认证方式指南](doc/authentication-guide.md)。

要切换认证方式，修改 `app/main.py` 中的 `auth_type` 参数：

```python
# 使用 Legacy Token (默认)
ls_client = LabelStudioClient(
    base_url=settings.label_studio_base_url,
    user_token=settings.label_studio_user_token,
    auth_type="token"
)

# 或使用 JWT Token
ls_client = LabelStudioClient(
    base_url=settings.label_studio_base_url,
    api_key=settings.label_studio_api_key,
    auth_type="jwt"
)
```


## 快速开始

### 使用Docker Compose

1. 启动所有服务：
```bash
docker-compose up -d
```

2. 查看日志：
```bash
docker-compose logs -f adapter
```

### 本地开发

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置环境变量（复制.env文件并修改）

3. 初始化项目：
```bash
python scripts/init_project.py
```

4. 启动服务：
```bash
python main.py
```

## API接口

### 1. 创建数据集映射

**POST** `/datasets/create`

创建DM数据集与Label Studio项目之间的映射关系。

**请求体**:
```json
{
  "source_dataset_uuid": "dm-dataset-uuid-here"
}
```

**响应**:
```json
{
  "mapping_uuid": "generated-mapping-uuid",
  "labelling_dataset_id": "label-studio-project-id",
  "message": "Dataset mapping created successfully"
}
```

### 2. 同步数据集内容

**POST** `/datasets/{source_dataset_uuid}/sync`

将DM数据集中的文件同步到Label Studio项目中。

**响应**:
```json
{
  "mapping_uuid": "mapping-uuid",
  "status": "success",
  "synced_files": 42,
  "message": "Successfully synced 42 files"
}
```

### 3. 删除数据集映射

**DELETE** `/datasets/mapping/{mapping_uuid}`

删除Label Studio项目并软删除映射关系。

**响应**:
```json
{
  "mapping_uuid": "mapping-uuid",
  "status": "success",
  "message": "Dataset mapping deleted successfully"
}
```

### 4. 查询映射关系

**GET** `/datasets/mappings` - 获取所有映射关系
**GET** `/datasets/mappings/{mapping_uuid}` - 获取指定映射关系

## 数据库结构

### dataset_mappings表

| 字段                   | 类型     | 说明                           |
| ---------------------- | -------- | ------------------------------ |
| uuid                   | String   | 主键，映射UUID                 |
| source_dataset_uuid    | String   | 源数据集UUID（DM系统）         |
| labelling_dataset_uuid | String   | 标注数据集UUID（Label Studio） |
| created_at             | DateTime | 创建时间                       |
| last_updated_at        | DateTime | 最后更新时间                   |
| deleted_at             | DateTime | 软删除时间（可空）             |

## 开发说明

### 项目结构

```
label-studio-adapter/
├── app/                      # 应用程序主目录
│   ├── api/                  # API路由层
│   │   ├── datasets.py       # 数据集相关API
│   │   └── system.py         # 系统相关API
│   ├── clients/             # 外部服务客户端
│   │   ├── dm_client.py      # 数据管理服务客户端
│   │   └── label_studio_client.py  # Label Studio客户端
│   ├── core/                # 核心配置和工具
│   │   ├── config.py         # 应用配置
│   │   └── logging.py        # 日志配置
│   ├── db/                  # 数据库相关
│   │   └── database.py       # 数据库连接和配置
│   ├── models/              # 数据库模型
│   │   └── dataset_mapping.py  # 数据集映射模型
│   ├── schemas/             # Pydantic数据模型
│   │   ├── dataset_mapping.py  # 映射相关模型
│   │   ├── dm_service.py     # DM服务模型
│   │   └── label_studio.py  # Label Studio模型
│   └── services/            # 业务逻辑服务
│       ├── dataset_mapping_service.py  # 映射服务
│       └── sync_service.py   # 同步服务
├── tests/                   # 测试文件
├── scripts/                 # 脚本文件
├── alembic/                 # 数据库迁移
├── doc/                     # 文档
├── main.py                  # 应用程序入口
├── requirements.txt         # Python依赖
├── .env                     # 环境变量配置
├── docker-compose.yml       # Docker Compose配置
└── README.md               # 项目说明
```

### 数据库迁移

生成迁移脚本：
```bash
alembic revision --autogenerate -m "Initial migration"
```

执行迁移：
```bash
alembic upgrade head
```

### 错误处理

- 404: 资源不存在（数据集、映射关系等）
- 400: 请求参数错误或重复创建
- 500: 内部服务器错误

### 日志

应用使用Python标准logging模块，日志级别可通过环境变量配置。

## 注意事项

1. 确保DM服务和Label Studio服务可访问
2. 数据库连接配置正确
3. Label Studio的标注配置可能需要根据实际数据类型调整
4. 文件同步依赖于DM服务提供的文件下载接口

## 许可证

MIT License