# Label Studio 认证方式指南

Label Studio Adapter 支持两种 Label Studio API 认证方式：

## 1. Legacy Token 认证（默认）

这是推荐的认证方式，使用 `Authorization: Token {token}` 头部进行认证。

### 配置方式

在 `.env` 文件中设置：

```properties
LABEL_STUDIO_USER_TOKEN="your-legacy-token-here"
```

### 获取 Legacy Token

1. 登录 Label Studio
2. 访问账户设置页面
3. 在 API Token 部分复制你的 token

### 使用方式

默认情况下，adapter 会使用 legacy token 认证：

```python
# 在 main.py 中，客户端默认使用 legacy token
ls_client = LabelStudioClient(
    base_url=settings.label_studio_base_url,
    user_token=settings.label_studio_user_token,
    auth_type="token"  # 使用 legacy token
)
```

## 2. JWT Token 认证（备用）

这种方式使用 JWT refresh token 进行认证。

### 配置方式

在 `.env` 文件中设置：

```properties
LABEL_STUDIO_API_KEY="your-jwt-refresh-token-here"
```

### 使用方式

如果需要使用 JWT 认证，修改 `main.py` 中的初始化代码：

```python
ls_client = LabelStudioClient(
    base_url=settings.label_studio_base_url,
    api_key=settings.label_studio_api_key,
    auth_type="jwt"  # 使用 JWT 认证
)
```

## 在运行时切换认证方式

客户端支持在运行时切换认证方式：

```python
from app.clients.client_manager import get_ls_client

# 获取客户端实例
ls_client = get_ls_client()

# 切换到 legacy token 认证
ls_client.switch_auth_type("token", "your-legacy-token")

# 切换到 JWT 认证
ls_client.switch_auth_type("jwt", "your-jwt-token")

# 查看当前认证方式
current_auth = ls_client.get_current_auth_type()
print(f"当前认证方式: {current_auth}")
```

## 认证方式对比

| 特性     | Legacy Token                   | JWT Token                       |
| -------- | ------------------------------ | ------------------------------- |
| 头部格式 | `Authorization: Token {token}` | `Authorization: Bearer {token}` |
| 过期时间 | 不过期（除非手动撤销）         | 有过期时间                      |
| 安全性   | 中等                           | 较高                            |
| 配置难度 | 简单                           | 较复杂                          |
| 推荐场景 | 开发环境、简单部署             | 生产环境、需要定期刷新token     |

## 启动参数配置

如果你修改了 Label Studio 的启动命令以支持 legacy token 认证（禁用 JWT），请确保：

1. Label Studio 启动时启用了 token 认证
2. 在 `.env` 中正确配置了 `LABEL_STUDIO_USER_TOKEN`
3. 在 `main.py` 中将 `auth_type` 设置为 `"token"`

## 故障排查

### 认证失败

1. 检查 token 是否正确配置在 `.env` 文件中
2. 确认 Label Studio 服务支持对应的认证方式
3. 查看日志中的认证方式提示信息

### 切换认证方式无效

1. 确保调用了 `switch_auth_type()` 方法
2. 验证提供的 token 是否有效
3. 重启服务以应用新的配置

## 最佳实践

1. **开发环境**：使用 legacy token，配置简单，便于调试
2. **生产环境**：建议使用 JWT token，安全性更高
3. **Token 管理**：将敏感的 token 存储在环境变量或密钥管理服务中
4. **定期更新**：定期更新和轮换 token 以提高安全性
