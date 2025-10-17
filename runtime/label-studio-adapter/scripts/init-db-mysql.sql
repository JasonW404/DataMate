-- 初始化Label Studio Adapter数据库 (MySQL版本)
-- 这个脚本会在MySQL容器首次启动时执行

-- 创建数据库 (如果不存在) - 通常由docker-compose环境变量处理
-- CREATE DATABASE IF NOT EXISTS label_studio_adapter CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE label_studio_adapter;

-- 设置默认时区为UTC
SET time_zone = '+00:00';

-- 确保使用utf8mb4字符集以支持完整的Unicode
ALTER DATABASE label_studio_adapter CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 输出初始化完成信息
SELECT 'Label Studio Adapter MySQL database initialized successfully!' as message;