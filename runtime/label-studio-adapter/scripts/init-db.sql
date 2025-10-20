-- 初始化Label Studio Adapter数据库
-- 这个脚本会在PostgreSQL容器首次启动时执行

-- 创建数据库 (如果不存在)
-- CREATE DATABASE labelstudio_adapter;

-- 连接到数据库
\c labelstudio_adapter;

-- 创建扩展 (如果需要)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 设置时区
SET timezone = 'UTC';

-- 创建应用程序用户权限
GRANT ALL PRIVILEGES ON DATABASE labelstudio_adapter TO "user";

-- 输出初始化完成信息
SELECT 'Label Studio Adapter database initialized successfully!' as message;