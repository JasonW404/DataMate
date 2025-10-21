# 安装

## 前置条件

- Git (用于源码安装)
- Docker (用于构建镜像和部署服务)
- Docker-Compose (用于部署服务)
- kubernetes (用于部署服务)
- Helm (用于部署服务)

```bash
# 拉取代码
git clone git@github.com:ModelEngine-Group/data-meta.git
```

## 镜像构建

```bash
make build
```

## Docker安装

```bash
make install INSTALLER=docker
```

## kubernetes安装

```bash
make install INSTALLER=k8s
```