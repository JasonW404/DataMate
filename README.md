# DataMate 一站式数据工作平台

[![Frontend Docker Image CI](https://github.com/ModelEngine-Group/DataMate/actions/workflows/docker-image-frontend.yml/badge.svg)](https://github.com/ModelEngine-Group/DataMate/actions/workflows/docker-image-frontend.yml)

[![Backend Docker Image CI](https://github.com/ModelEngine-Group/DataMate/actions/workflows/docker-image-backend.yml/badge.svg)](https://github.com/ModelEngine-Group/DataMate/actions/workflows/docker-image-backend.yml)

![GitHub Stars](https://img.shields.io/github/stars/ModelEngine-Group/DataMate)
![GitHub Forks](https://img.shields.io/github/forks/ModelEngine-Group/DataMate)
![GitHub Issues](https://img.shields.io/github/issues/ModelEngine-Group/DataMate)
![GitHub License](https://img.shields.io/github/license/ModelEngine-Group/DataMate)

[简体中文](./README-zh.md) | English

> DataMate是面向模型微调与RAG检索的企业级数据处理平台，支持数据管理、算子市场、数据清洗、数据合成、数据标注、数据评估等核心功能。

## 🌟 核心特性

- **六大核心模块**：数据管理、算子市场、数据清洗、数据合成、数据标注、数据评估
- **DDD架构**：领域驱动设计，清晰的分层架构
- **微服务架构**：Spring Boot + 容器化部署
- **可视化编排**：拖拽式数据处理流程设计
- **算子生态**：丰富的内置算子和自定义算子支持

## 🚀 快速开始

### 前置条件

- Git (用于拉取源码)
- Make (用于构建和安装)
- Docker (用于构建镜像和部署服务)
- Docker-Compose (用于部署服务-docker方式)
- kubernetes (用于部署服务-k8s方式)
- Helm (用于部署服务-k8s方式)

### 拉取代码

```bash
git clone git@github.com:ModelEngine-Group/data-mate.git
```

### 镜像构建

```bash
make build
```

### Docker安装

```bash
make install INSTALLER=docker
```

### kubernetes安装

```bash
make install INSTALLER=k8s
```

## 🤝 贡献指南

感谢您对本项目的关注！我们非常欢迎社区的贡献，无论是提交 Bug 报告、提出功能建议，还是直接参与代码开发，都能帮助项目变得更好。

• 📮 [GitHub Issues](../../issues)：提交 Bug 或功能建议。

• 🔧 [GitHub Pull Requests](../../pulls)：贡献代码改进。

## 📄 许可证

DataMate 基于 [MIT](LICENSE) 开源，您可以在遵守许可证条款的前提下自由使用、修改和分发本项目的代码。
