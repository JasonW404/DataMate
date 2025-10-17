# 开发指南

## 项目结构

```
label-studio-adapter/
├── app/                      # 应用程序主目录
│   ├── __init__.py
│   ├── api/                  # API路由层
│   │   ├── __init__.py
│   │   ├── datasets.py       # 数据集相关API
│   │   └── system.py         # 系统相关API
│   ├── clients/             # 外部服务客户端
│   │   ├── __init__.py
│   │   ├── dm_client.py      # 数据管理服务客户端
│   │   └── label_studio_client.py  # Label Studio客户端
│   ├── core/                # 核心配置和工具
│   │   ├── __init__.py
│   │   ├── config.py         # 应用配置
│   │   └── logging.py        # 日志配置
│   ├── db/                  # 数据库相关
│   │   ├── __init__.py
│   │   └── database.py       # 数据库连接和配置
│   ├── models/              # 数据库模型
│   │   ├── __init__.py
│   │   └── dataset_mapping.py  # 数据集映射模型
│   ├── schemas/             # Pydantic数据模型
│   │   ├── __init__.py
│   │   ├── dataset_mapping.py  # 映射相关模型
│   │   ├── dm_service.py     # DM服务模型
│   │   └── label_studio.py  # Label Studio模型
│   └── services/            # 业务逻辑服务
│       ├── __init__.py
│       ├── dataset_mapping_service.py  # 映射服务
│       └── sync_service.py   # 同步服务
├── tests/                   # 测试文件
│   ├── __init__.py
│   ├── conftest.py          # 测试配置
│   └── test_services.py     # 服务测试
├── scripts/                 # 脚本文件
│   ├── init_project.py      # 项目初始化脚本
│   └── test_api.py          # API测试脚本
├── alembic/                 # 数据库迁移
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── logs/                    # 日志文件目录
├── doc/                     # 文档
├── ref/                     # 参考文件
├── main.py                  # 应用程序入口
├── requirements.txt         # Python依赖
├── .env                     # 环境变量配置
├── alembic.ini             # 数据库迁移配置
├── docker-compose.yml       # Docker Compose配置
├── Dockerfile              # Docker镜像构建
└── README.md               # 项目说明
```

## 架构设计

### 分层架构

1. **API层** (`app/api/`)
   - 处理HTTP请求和响应
   - 数据验证和序列化
   - 异常处理

2. **服务层** (`app/services/`)
   - 业务逻辑实现
   - 数据处理和转换
   - 外部服务调用协调

3. **数据访问层** (`app/models/`, `app/db/`)
   - 数据库模型定义
   - 数据库操作

4. **客户端层** (`app/clients/`)
   - 外部服务API调用
   - 网络请求封装

### 设计模式

- **依赖注入**: 使用FastAPI的Depends系统
- **服务层模式**: 业务逻辑与API分离
- **资源库模式**: 数据访问抽象
- **客户端模式**: 外部服务调用封装

## 开发工作流

### 1. 添加新功能

1. **定义数据模型** (`app/schemas/`)
2. **创建数据库模型** (`app/models/`)
3. **实现服务逻辑** (`app/services/`)
4. **创建API端点** (`app/api/`)
5. **编写测试** (`tests/`)
6. **更新文档**

### 2. 数据库变更

```bash
# 生成迁移文件
alembic revision --autogenerate -m "描述变更"

# 执行迁移
alembic upgrade head
```

### 3. 测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_services.py

# 测试覆盖率
pytest --cov=app
```

### 4. 代码质量

```bash
# 代码格式化
black app/
isort app/

# 类型检查
mypy app/

# 代码检查
flake8 app/
```

## 配置管理

### 环境变量

所有配置通过环境变量或`.env`文件管理，配置定义在`app/core/config.py`中。

### 配置优先级

1. 环境变量
2. `.env`文件
3. 默认值

## 日志管理

### 日志配置

日志配置在`app/core/logging.py`中，支持：
- 控制台输出
- 文件输出
- 不同级别的日志分离

### 使用方法

```python
from app.core.logging import get_logger

logger = get_logger(__name__)
logger.info("信息日志")
logger.error("错误日志")
```

## 错误处理

### 异常层次

1. **HTTP异常**: FastAPI HTTPException
2. **业务异常**: 自定义业务异常
3. **系统异常**: 系统级错误

### 错误响应格式

```json
{
    "detail": "错误描述",
    "error_code": "错误代码",
    "timestamp": "2025-10-09T10:00:00Z"
}
```

## 性能优化

### 数据库优化

- 使用异步数据库操作
- 合理的索引设计
- 连接池管理

### 网络优化

- HTTP连接复用
- 请求超时控制
- 批量操作支持

### 缓存策略

- 响应缓存
- 数据库查询缓存
- 外部服务调用缓存

## 部署指南

### Docker部署

```bash
# 构建镜像
docker build -t label-studio-adapter .

# 运行容器
docker-compose up -d
```

### 生产环境

1. 设置合适的环境变量
2. 配置反向代理（Nginx）
3. 设置监控和日志收集
4. 配置健康检查
5. 设置自动重启

## 扩展指南

### 添加新的外部服务

1. 在`app/clients/`中创建客户端
2. 在`app/schemas/`中定义数据模型
3. 在服务层中集成调用
4. 更新配置和文档

### 添加新的API端点

1. 在`app/api/`中创建路由文件
2. 在`main.py`中注册路由
3. 编写对应的服务逻辑
4. 添加测试用例

### 数据库扩展

1. 在`app/models/`中添加新模型
2. 生成并执行数据库迁移
3. 更新服务层逻辑
4. 更新API接口

## 最佳实践

### 代码规范

- 使用类型提示
- 遵循PEP 8规范
- 编写清晰的注释和文档字符串
- 使用有意义的变量和函数名

### 安全考虑

- 输入验证和清理
- API访问控制
- 敏感信息加密
- SQL注入防护

### 性能考虑

- 异步编程
- 合理的超时设置
- 资源池管理
- 错误重试机制