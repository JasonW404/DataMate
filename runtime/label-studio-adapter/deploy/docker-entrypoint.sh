#!/bin/bash
set -e

echo "=========================================="
echo "Label Studio Adapter Starting..."
echo "=========================================="

# 加载 .env 文件（如果存在）
if [ -f .env ]; then
    echo "Loading environment variables from .env file..."
    export $(cat .env | grep -v '^#' | grep -v '^$' | xargs)
fi

# # 等待数据库就绪（如果配置了数据库）
# if [ -n "$MYSQL_HOST" ] || [ -n "$POSTGRES_HOST" ]; then
#     echo "Waiting for database to be ready..."
#     sleep 5
# fi

# # 运行数据库迁移
# echo "Running database migrations..."
# alembic upgrade head

# 启动应用
echo "Starting Label Studio Adapter..."
echo "Host: ${HOST:-0.0.0.0}"
echo "Port: ${PORT:-18000}"
echo "Debug: ${DEBUG:-false}"
echo "Label Studio URL: ${LABEL_STUDIO_BASE_URL}"
echo "=========================================="

# 使用 uvicorn 启动应用
exec uvicorn app.main:app \
    --host "${HOST:-0.0.0.0}" \
    --port "${PORT:-18000}" \
    --log-level "${LOG_LEVEL:-info}" \
    ${DEBUG:+--reload}
