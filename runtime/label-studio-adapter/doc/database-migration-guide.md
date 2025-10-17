# 数据库切换指南

## 概述

本项目采用以下数据库架构：
- **Adapter**: 使用 **MySQL** 数据库
- **Label Studio**: 使用 **PostgreSQL** 数据库

两个系统使用独立的数据库，互不干扰。

## 架构说明

```
┌─────────────────────┐
│   Adapter Service   │
│   (FastAPI)         │
└──────────┬──────────┘
           │
           ▼
    ┌──────────────┐
    │    MySQL     │  ← Adapter专用数据库
    │   (Port 3306)│
    └──────────────┘

┌─────────────────────┐
│  Label Studio App   │
└──────────┬──────────┘
           │
           ▼
    ┌──────────────┐
    │  PostgreSQL  │  ← Label Studio专用数据库
    │   (Port 5432)│
    └──────────────┘
```

## 配置文件

### 1. 环境变量配置 (`.env`)

```bash
# Adapter数据库配置 (MySQL)
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=label_studio_user
MYSQL_PASSWORD=user_password
MYSQL_DATABASE=label_studio_adapter

# Label Studio数据库配置 (Postgres) - 仅供参考
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=labelstudio
POSTGRES_PASSWORD=password
POSTGRES_DATABASE=labelstudio
```

### 2. 配置优先级

`app/core/config.py` 实现了智能数据库选择机制：

1. **优先级1**: MySQL（如果配置了 `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`）
2. **优先级2**: PostgreSQL（如果MySQL未配置但配置了Postgres参数）
3. **优先级3**: SQLite（兜底方案，用于开发/测试）

当前配置会自动选择MySQL作为Adapter的数据库。

## 数据库初始化

### 方式一：使用Docker Compose（推荐）

1. **启动MySQL数据库**:
```bash
docker-compose -f docker-compose.yml -f docker-compose.mysql.yml up -d adapter-mysql
```

2. **等待MySQL启动完成**:
```bash
docker-compose -f docker-compose.yml -f docker-compose.mysql.yml ps
```

3. **运行数据库迁移**:
```bash
# 在本地环境
alembic upgrade head

# 或在Docker容器中
docker-compose exec adapter alembic upgrade head
```

### 方式二：使用本地MySQL

1. **确保MySQL正在运行**:
```bash
mysql --version
# 或检查服务状态
brew services list | grep mysql  # macOS
```

2. **创建数据库和用户**:
```bash
mysql -u root -p
```

```sql
-- 创建数据库
CREATE DATABASE label_studio_adapter CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建用户
CREATE USER 'label_studio_user'@'localhost' IDENTIFIED BY 'user_password';

-- 授权
GRANT ALL PRIVILEGES ON label_studio_adapter.* TO 'label_studio_user'@'localhost';
FLUSH PRIVILEGES;

-- 退出
EXIT;
```

3. **运行数据库迁移**:
```bash
alembic upgrade head
```

## 验证配置

### 1. 运行验证脚本

```bash
python scripts/check_db_config.py
```

此脚本会检查：
- ✅ 数据库配置是否正确
- ✅ 是否使用MySQL
- ✅ 数据库连接是否正常
- ✅ 迁移状态

### 2. 手动验证

```bash
# 测试MySQL连接
mysql -h localhost -u label_studio_user -p label_studio_adapter

# 查看表结构
mysql> SHOW TABLES;
mysql> DESCRIBE dataset_mappings;
```

## MySQL vs PostgreSQL 兼容性调整

### 已修复的兼容性问题

1. **时间戳函数**:
   - PostgreSQL: `now()`
   - MySQL: `CURRENT_TIMESTAMP`
   - ✅ 已在迁移脚本中修复

2. **字符串长度**:
   - PostgreSQL: `String()` 可以不指定长度
   - MySQL: `String(length)` 必须指定长度
   - ✅ 已在迁移脚本中修复（UUID字段使用 `String(36)`）

3. **时区支持**:
   - 两者都支持 `DateTime(timezone=True)`
   - ✅ 配置正确

### SQLAlchemy模型（无需修改）

模型定义 (`app/models/dataset_mapping.py`) 使用了跨数据库兼容的语法：
- `func.now()` - SQLAlchemy会自动转换为对应数据库的函数
- `String(36)` - 明确指定长度
- `DateTime(timezone=True)` - 跨数据库时区支持

## 迁移脚本说明

### 当前迁移

**版本**: `1597600460eb_create_dataset_mapping_table.py`

**修改内容**:
```python
# ✅ MySQL兼容版本
sa.Column('uuid', sa.String(36), nullable=False)  # 指定长度
sa.Column('created_at', sa.DateTime(timezone=True), 
          server_default=sa.text('CURRENT_TIMESTAMP'),  # MySQL兼容
          nullable=True, comment='创建时间')
```

**原始问题**:
```python
# ❌ PostgreSQL特定语法
sa.Column('uuid', sa.String(), nullable=False)  # MySQL需要长度
sa.Column('created_at', sa.DateTime(timezone=True), 
          server_default=sa.text('now()'),  # PostgreSQL特定
          nullable=True, comment='创建时间')
```

### 创建新迁移

```bash
# 修改模型后生成迁移
alembic revision --autogenerate -m "描述变更"

# 应用迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1
```

## Docker Compose配置

### Adapter服务

```yaml
adapter:
  environment:
    # ✅ 使用MySQL配置
    MYSQL_HOST: ${MYSQL_HOST}
    MYSQL_PORT: ${MYSQL_PORT}
    MYSQL_USER: ${MYSQL_USER}
    MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    MYSQL_DATABASE: ${MYSQL_DATABASE}
```

### Label Studio服务（无需修改）

```yaml
label-studio:
  environment:
    # Label Studio继续使用PostgreSQL
    POSTGRE_HOST: ${COMPOSE_PROJECT_NAME:-ls-adapter}_ls-db
    POSTGRE_NAME: labelstudio
    POSTGRE_USER: labelstudio
    POSTGRE_PASSWORD: labelstudio@4321
```

## 故障排查

### 问题1: 连接失败

**错误**: `Can't connect to MySQL server`

**解决**:
1. 检查MySQL是否运行: `mysql --version`
2. 检查端口: `netstat -an | grep 3306`
3. 验证凭据: `mysql -h localhost -u label_studio_user -p`

### 问题2: 字符编码错误

**错误**: `Incorrect string value`

**解决**:
```sql
-- 确保数据库使用utf8mb4
ALTER DATABASE label_studio_adapter 
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 确保表使用utf8mb4
ALTER TABLE dataset_mappings 
  CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 问题3: 迁移失败

**错误**: `Target database is not up to date`

**解决**:
```bash
# 查看当前版本
alembic current

# 查看历史
alembic history

# 重置到基础版本
alembic downgrade base

# 重新应用所有迁移
alembic upgrade head
```

### 问题4: 时区问题

**错误**: 时间戳不正确

**解决**:
```sql
-- 设置MySQL时区为UTC
SET GLOBAL time_zone = '+00:00';
SET time_zone = '+00:00';
```

或在配置文件中 (`my.cnf`):
```ini
[mysqld]
default-time-zone='+00:00'
```

## 开发工作流

### 本地开发

1. 启动MySQL:
```bash
# macOS
brew services start mysql

# Docker
docker-compose -f docker-compose.mysql.yml up -d adapter-mysql
```

2. 运行迁移:
```bash
alembic upgrade head
```

3. 启动应用:
```bash
uvicorn app.main:app --reload
```

### Docker开发

```bash
# 启动所有服务（包括MySQL）
docker-compose -f docker-compose.yml -f docker-compose.mysql.yml up

# 仅启动Adapter和MySQL
docker-compose -f docker-compose.yml -f docker-compose.mysql.yml up adapter adapter-mysql
```

## 数据备份

### MySQL备份

```bash
# 导出数据
mysqldump -u label_studio_user -p label_studio_adapter > backup.sql

# 导入数据
mysql -u label_studio_user -p label_studio_adapter < backup.sql
```

### Docker环境备份

```bash
# 导出容器数据
docker exec adapter-mysql mysqldump -u root -proot_password label_studio_adapter > backup.sql

# 导入到容器
docker exec -i adapter-mysql mysql -u root -proot_password label_studio_adapter < backup.sql
```

## 性能优化建议

### MySQL配置优化

1. **连接池配置**:
```python
# app/db/database.py
engine = create_async_engine(
    settings.computed_database_url,
    pool_size=20,        # 连接池大小
    max_overflow=10,     # 超出连接数
    pool_recycle=3600,   # 连接回收时间
    echo=False
)
```

2. **索引优化**:
```sql
-- 为常用查询添加索引
CREATE INDEX idx_source_uuid ON dataset_mappings(source_dataset_uuid);
CREATE INDEX idx_created_at ON dataset_mappings(created_at);
CREATE INDEX idx_deleted_at ON dataset_mappings(deleted_at);
```

## 参考资料

- [SQLAlchemy文档](https://docs.sqlalchemy.org/)
- [Alembic文档](https://alembic.sqlalchemy.org/)
- [MySQL文档](https://dev.mysql.com/doc/)
- [Label Studio文档](https://labelstud.io/guide/)
