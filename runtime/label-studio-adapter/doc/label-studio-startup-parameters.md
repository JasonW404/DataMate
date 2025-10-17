# Label Studio 启动参数配置指南

## 概述

Label Studio 支持通过命令行参数自定义启动配置。在 Docker 环境中，可以通过 `command` 字段传递这些参数。

## Docker 容器配置

### Entrypoint 和 Command

```yaml
# Label Studio 官方镜像配置
Entrypoint: ./deploy/docker-entrypoint.sh
Cmd: label-studio
```

**工作原理**：
1. 容器启动时执行 `docker-entrypoint.sh` 脚本
2. 脚本会运行 `label-studio` 命令及您提供的参数
3. 通过 `command` 字段可以覆盖默认的 `Cmd`

## 常用启动参数

### 基础参数

```bash
label-studio start [OPTIONS]
```

| 参数                  | 说明             | 默认值                        | 示例                                |
| --------------------- | ---------------- | ----------------------------- | ----------------------------------- |
| `--host HOST`         | 绑定的主机地址   | `localhost`                   | `0.0.0.0`                           |
| `--port PORT`         | 端口号           | `8080`                        | `8080`                              |
| `--data-dir DIR`      | 数据存储目录     | `~/.local/share/label-studio` | `/label-studio/data`                |
| `--log-level LEVEL`   | 日志级别         | `INFO`                        | `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `--database DATABASE` | 数据库类型       | `default` (SQLite)            | `default`, `postgresql`             |
| `--username USERNAME` | 初始管理员用户名 | -                             | `admin@example.com`                 |
| `--password PASSWORD` | 初始管理员密码   | -                             | `password123`                       |

### 高级参数

| 参数                  | 说明             | 示例                                        |
| --------------------- | ---------------- | ------------------------------------------- |
| `--debug`             | 启用调试模式     | -                                           |
| `--no-browser`        | 不自动打开浏览器 | -                                           |
| `--cert FILE`         | SSL 证书文件     | `/path/to/cert.pem`                         |
| `--key FILE`          | SSL 密钥文件     | `/path/to/key.pem`                          |
| `--label-config FILE` | 默认标注配置文件 | `/path/to/config.xml`                       |
| `--sampling STRATEGY` | 任务采样策略     | `sequential`, `uniform`, `prediction-score` |

## Docker Compose 配置示例

### 示例 1：基础配置

```yaml
services:
  label-studio:
    image: heartexlabs/label-studio:latest
    command: >
      label-studio start
      --host 0.0.0.0
      --port 8080
      --log-level INFO
```

### 示例 2：调试模式

```yaml
services:
  label-studio:
    image: heartexlabs/label-studio:latest
    command: >
      label-studio start
      --host 0.0.0.0
      --port 8080
      --log-level DEBUG
      --debug
```

### 示例 3：自定义数据目录和日志级别

```yaml
services:
  label-studio:
    image: heartexlabs/label-studio:latest
    volumes:
      - label_studio_data:/label-studio/data
    command: >
      label-studio start
      --host 0.0.0.0
      --port 8080
      --data-dir /label-studio/data
      --log-level ${LOG_LEVEL:-INFO}
```

### 示例 4：使用环境变量

```yaml
services:
  label-studio:
    image: heartexlabs/label-studio:latest
    environment:
      LOG_LEVEL: DEBUG
    command: >
      label-studio start
      --host 0.0.0.0
      --port 8080
      --log-level ${LOG_LEVEL}
```

## 当前项目配置

在 `docker-compose.label-studio.yml` 中的配置：

```yaml
services:
  label-studio:
    image: heartexlabs/label-studio:latest
    environment:
      # 环境变量配置（优先级更高）
      LABEL_STUDIO_HOST: ${LABEL_STUDIO_BASE_URL:-http://localhost:8000}
      LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED: "true"
      LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT: /label-studio/local_files
      # ... 其他环境变量
    volumes:
      - label_studio_data:/label-studio/data
      - label_studio_local:/label-studio/local_files
    command: >
      label-studio start
      --host 0.0.0.0
      --port 8080
      --log-level ${LOG_LEVEL:-INFO}
      --data-dir /label-studio/data
```

## 环境变量 vs 命令行参数

### 优先级

1. **命令行参数** > 环境变量 > 配置文件
2. 如果同时设置，命令行参数会覆盖环境变量

### 环境变量映射

Label Studio 支持通过环境变量配置，命名规则：

```bash
# 命令行参数
--log-level INFO

# 对应的环境变量
LABEL_STUDIO_LOG_LEVEL=INFO

# 或使用 Django 设置
LOG_LEVEL=INFO
```

常用环境变量：

| 环境变量                                   | 对应参数      | 说明             |
| ------------------------------------------ | ------------- | ---------------- |
| `LABEL_STUDIO_HOST`                        | `--host`      | 主机地址         |
| `LABEL_STUDIO_PORT`                        | `--port`      | 端口号           |
| `LABEL_STUDIO_LOG_LEVEL`                   | `--log-level` | 日志级别         |
| `LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED` | -             | 启用本地文件服务 |
| `LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT`   | -             | 本地文件根目录   |

## 常见配置场景

### 场景 1：开发环境（调试模式）

```yaml
command: >
  label-studio start
  --host 0.0.0.0
  --port 8080
  --log-level DEBUG
  --debug
```

### 场景 2：生产环境（PostgreSQL）

```yaml
environment:
  DJANGO_DB: default
  POSTGRE_HOST: postgres
  POSTGRE_PORT: 5432
  POSTGRE_NAME: labelstudio
  POSTGRE_USER: labelstudio
  POSTGRE_PASSWORD: password
command: >
  label-studio start
  --host 0.0.0.0
  --port 8080
  --log-level WARNING
  --data-dir /label-studio/data
```

### 场景 3：本地文件支持

```yaml
environment:
  LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED: "true"
  LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT: /data/local-files
volumes:
  - ./local-files:/data/local-files:ro
command: >
  label-studio start
  --host 0.0.0.0
  --port 8080
  --log-level INFO
```

## 验证配置

### 1. 查看容器日志

```bash
docker logs label-studio-adapter_ls-app
```

### 2. 检查启动参数

```bash
docker inspect label-studio-adapter_ls-app --format='{{.Config.Cmd}}'
```

### 3. 进入容器检查进程

```bash
docker exec -it label-studio-adapter_ls-app ps aux | grep label-studio
```

## 故障排查

### 问题 1：参数不生效

**原因**：环境变量优先级更高

**解决**：
1. 移除冲突的环境变量
2. 或确保命令行参数值不同

### 问题 2：容器启动失败

**检查**：
```bash
# 查看详细日志
docker logs label-studio-adapter_ls-app

# 检查配置语法
docker-compose config
```

### 问题 3：参数格式错误

**正确格式**：
```yaml
# ✅ 正确 - 使用 > 符号和换行
command: >
  label-studio start
  --host 0.0.0.0
  --port 8080

# ✅ 正确 - 单行
command: "label-studio start --host 0.0.0.0 --port 8080"

# ✅ 正确 - 数组格式
command:
  - label-studio
  - start
  - --host
  - 0.0.0.0
  - --port
  - "8080"

# ❌ 错误 - 缺少引号导致解析错误
command: label-studio start --host 0.0.0.0
```

## 参考资料

- [Label Studio 官方文档](https://labelstud.io/guide/start)
- [Label Studio Docker Hub](https://hub.docker.com/r/heartexlabs/label-studio)
- [Label Studio GitHub](https://github.com/heartexlabs/label-studio)
- [Docker Compose Command 文档](https://docs.docker.com/compose/compose-file/05-services/#command)
