# Data-Engine 一站式数据工作平台架构设计

## 整体目录结构

### 完整平台目录架构
基于"六大核心模块 + DDD分层 + 双版本（开源/商业）"的完整目录组织：

```
data-engine-platform/
├── docs/                               # 📖 文档中心
│   ├── architecture/                   # 架构与设计文档
│   │   ├── 一站式数据工作平台特性设计.md
│   │   ├── 代码架构设计.md
│   │   ├── 算子市场架构设计.md
│   │   ├── 部署配置方案.md
│   │   └── 部署视图总结.md
│   ├── api/                           # API文档 (OpenAPI/Swagger)
│   ├── user-guide/                    # 用户/运维/开发指南  
│   ├──operator-performance/                        # 算子性能报告
│   └── ops/                           # 运维规程与应急预案
│
├── frontend/                           # 🎨 前端应用
│   ├── apps/                          # 多前端应用
│   │   ├── console/                   # 数据工作台&运营控制台
│   │   │   ├── next.config.js
│   │   │   ├── package.json
│   │   │   └── src/
│   │   └── annotation-studio/         # 标注工作台（可分离部署）
│   ├── packages/                      # 共享UI组件/SDK
│   └── config/                        # 构建与环境配置
│
├── backend/                            # 🔧 后端服务架构
│   ├── api-gateway/                   # API网关微服务 (独立部署)
│   │   ├── src/main/java/com/dataengine/gateway/
│   │   │   ├── auth/                  # 认证授权模块
│   │   │   ├── routing/               # 路由转发模块
│   │   │   ├── filter/                # 过滤器链
│   │   │   └── config/                # 网关配置
│   │   └── pom.xml
│   │
│   ├── services/                      # 业务服务目录
│   │   ├── main-application/          # 主应用微服务 (聚合器)
│   │   │   ├── src/main/java/com/dataengine/
│   │   │   └── pom.xml               # 依赖所有业务服务JAR
│   │   │
│   │   ├── data-management-service/   # 数据管理服务 (JAR包)
│   │   │   ├── domain/               # DDD领域层
│   │   │   ├── application/          # DDD应用层
│   │   │   ├── infrastructure/       # DDD基础设施层
│   │   │   └── interfaces/           # DDD接口层 (OpenAPI生成)
│   │   │
│   │   ├── operator-market-service/   # 算子市场服务 (JAR包)
│   │   ├── data-cleaning-service/     # 数据清洗服务 (JAR包)
│   │   ├── data-synthesis-service/    # 数据合成服务 (JAR包)
│   │   ├── data-annotation-service/   # 数据标注服务 (JAR包)
│   │   ├── data-evaluation-service/   # 数据评估服务 (JAR包)
│   │   ├── pipeline-orchestration-service/  # 流程编排服务 (JAR包)
│   │   ├── execution-engine-service/  # 执行引擎服务 (JAR包)
│   │   ├── rag-indexer-service/       # RAG索引服务 (JAR包)
│   │   └── rag-query-service/         # RAG查询服务 (JAR包)
│   │
│   └── shared/                        # 共享库与通用组件
│       ├── domain-common/             # 共享值对象、通用异常、规范
│       ├── security-common/           # JWT/OAuth2/RBAC
│       ├── monitoring-common/         # 指标、日志、链路追踪
│       └── storage-common/            # MinIO/S3/FS抽象
│
├── runtime/                            # 🚀 运行时与算子
│   ├── python-executor/               # Python执行器 (Ray Actor/Job)
│   │   ├── operator_runtime.py
│   │   ├── wrappers/                  # 各类算子包装器
│   │   │   ├── data_juicer_wrapper.py
│   │   │   ├── dingo_wrapper.py
│   │   │   ├── unstructured_io_wrapper.py
│   │   │   └── custom_operator_loader.py
│   │   └── requirements.txt
│   ├── datax/                         # DataX内置 (CE场景为Jar依赖)
│   └── operators/                     # 自定义算子仓库 (规范、模板、示例)
│       ├── README.md
│       └── examples/
│           └── text_length_filter/
│               ├── metadata.json
│               └── operator.py
│
├── openapi/                            # 📋 API规范定义
│   ├── specs/                         # OpenAPI 3.0规范文件
│   │   ├── data-management.yaml
│   │   ├── data-collection.yaml
│   │   ├── operator-market.yaml
│   │   ├── data-cleaning.yaml
│   │   ├── data-synthesis.yaml
│   │   ├── data-annotation.yaml
│   │   ├── data-evaluation.yaml
│   │   ├── pipeline-orchestration.yaml
│   │   ├── execution-engine.yaml
│   │   └── rag-services.yaml
│
├── deployment/                         # 🐳 部署与环境
│   ├── docker/                        # 通用Dockerfile与Compose模版
│   │   └── docker-compose.yml
│   ├── kubernetes/                    # 通用K8s清单
│   │   ├── api-gateway.yaml
│   │   └── mysql.yaml
│   ├── monitoring/                    # Prometheus/Grafana配置
│   └── scripts/                       # 部署脚本CI/CD钩子
│   └── db/                       #  数据库脚本 
│       └── data-management-init.sql  # 数据管理初始化
│
├── editions/                           # 📦 版本差异化配置
│   ├── community/                     # 社区版配置
│   │   ├── docker/                    # CE专属Dockerfile/Compose
│   │   │   └── docker-compose.yml
│   │   ├── k8s/                       # CE专属K8s清单
│   │   │   └── mysql.yaml
│   │   └── config/                    # CE专属应用配置
│   │       └── application.yml
│   └── enterprise/                    # 企业版配置
│       ├── docker/                    # EE专属Dockerfile/Compose
│       │   └── docker-compose.yml
│       ├── k8s/                       # EE专属K8s清单
│       └── config/                    # EE专属应用配置
│
├── monitoring/                         # 📊 监控与告警
│   ├── prometheus/
│   ├── grafana/
│   └── alerting/   
│
├── tests/                              # 🧪 自动化测试
│   ├── unit/                          # 单元测试
│   ├── integration/                   # 集成测试
│   ├── e2e/                           # 端到端测试
│   └── performance/                   # 性能测试、算子性能脚本
│
├── README.md                           # 项目说明
├── RELEASENOTE.md                        # 更新日志
├── LICENSE                             # 开源协议
└── pom.xml                            # Maven根配置
```

## 微服务架构设计

### 双微服务 + JAR包依赖架构
基于API First设计的混合架构模式：

```
┌─────────────────────────────────────────────────────────────────┐
│                      前端层 (Frontend)                          │
│  ┌─────────────────┐  ┌─────────────────────────────────────┐   │
│  │   数据工作台     │  │     标注工作台                      │   │
│  │   (Console)     │  │  (Annotation Studio)               │   │
│  └─────────────────┘  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                  │
                                  │ HTTP/HTTPS
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                    API网关微服务 (API Gateway)                   │
│           路由、鉴权、限流、监控 + 认证授权服务                   │
│              Port: 8080 (统一入口)                              │
└─────────────────────────────────────────────────────────────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
                    ▼             ▼             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     主应用微服务 (Main Application)              │
│                    Port: 8090 (服务聚合器)                     │
│                                                                 │
│  集成所有业务服务JAR包，提供统一的业务处理能力                   │
│                                                                 │
│  ┌─── JAR包依赖的业务服务模块 ───────────────────────────┐       │
│  │                                                       │       │
│  │  📦 data-management-service     (数据管理)            │       │
│  │  📦 data-collection-service     (数据归集)            │       │
│  │  📦 operator-market-service     (算子市场)            │       │
│  │  📦 data-cleaning-service       (数据清洗)            │       │
│  │  📦 data-synthesis-service      (数据合成)            │       │
│  │  📦 data-annotation-service     (数据标注)            │       │
│  │  📦 data-evaluation-service     (数据评估)            │       │
│  │  📦 pipeline-orchestration-service (流程编排)         │       │
│  │  📦 execution-engine-service    (执行引擎)            │       │
│  │  📦 rag-indexer-service         (RAG索引)             │       │
│  │  📦 rag-query-service           (RAG查询)             │       │
│  │                                                       │       │
│  └───────────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                    运行时环境 (Runtime)                          │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐    │
│  │Python执行器  │ │   DataX     │ │    自定义算子仓库        │    │
│  │(Ray Actor)  │ │  (内置Jar)   │ │  (规范/模板/示例)       │    │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## 六大核心模块映射

### 业务模块与服务对应关系

| 核心模块 | 微服务/JAR包 | 目录位置 | OpenAPI规范 | 说明 |
|---------|-------------|----------|-------------|------|
| 数据管理 | `data-management-service` | `backend/services/` | `data-management.yaml` | 元数据、血缘、治理 |
| 数据归集 | `data-collection-service` | `backend/services/` | `data-collection.yaml` | DataX数据归集、多源同步、ETL任务 |
| 算子市场 | `operator-market-service` | `backend/services/` | `operator-market.yaml` | 算子注册/发布/版本/评分/安装 |
| 数据清洗 | `data-cleaning-service` | `backend/services/` | `data-cleaning.yaml` | 文本/结构化/多媒体清洗策略 |
| 数据合成 | `data-synthesis-service` | `backend/services/` | `data-synthesis.yaml` | 指令、COT蒸馏、对话、多模态 |
| 数据标注 | `data-annotation-service` | `backend/services/` | `data-annotation.yaml` | 预标注、工作台、主动学习 |
| 数据评估 | `data-evaluation-service` | `backend/services/` | `data-evaluation.yaml` | 质量、适配性、价值评估 |
| 流程编排 | `pipeline-orchestration-service` | `backend/services/` | `pipeline-orchestration.yaml` | 拖拽编排、模板、依赖图 |
| 执行引擎 | `execution-engine-service` | `backend/services/` | `execution-engine.yaml` | 调度、任务编排、对接执行器 |
| RAG检索 | `rag-indexer-service`<br/>`rag-query-service` | `backend/services/` | `rag-services.yaml` | 知识库构建与检索增强 |

### 支撑服务

| 服务类型 | 微服务名称 | 部署形态 | 端口 | 说明 |
|---------|-----------|----------|------|------|
| 网关服务 | `api-gateway` | 独立微服务 | 8080 | 统一入口、鉴权、路由、限流 |
| 主应用 | `main-application` | 独立微服务 | 8090 | 业务聚合器，依赖所有JAR包 |
| 共享库 | `shared` | JAR包依赖 | - | 领域通用、安全、监控、存储 |

## 版本差异化架构

### 双版本部署策略

```
editions/
├── community/                    # 社区版 (CE)
│   ├── docker/                   # MySQL + Ray + OMS-CE
│   ├── k8s/                      # 基础K8s资源
│   └── config/                   # 开源配置
│
└── enterprise/                   # 企业版 (EE)
    ├── docker/                   # GaussDB + 九天 + OMS-EE
    ├── k8s/                      # 企业级K8s资源 eContainer
    └── config/                   # 企业配置 (License/审计)
```

### 技术栈对比

| 组件类型 | 社区版 (CE) | 企业版 (EE) |
|---------|------------|----------|
| 数据库 | MySQL 8.0 | GaussDB  |
| 计算引擎 | Ray 2.7 | 九天       |
| 底座	| OMS-LITE	|OMS   |

## 运行时架构

### Python执行器架构
位置：`runtime/python-executor/`

```
Python执行器 (Ray Actor/Job)
├── operator_runtime.py           # 统一执行入口
├── wrappers/                     # 算子包装器
│   ├── data_juicer_wrapper.py    # Data-Juicer集成
│   ├── dingo_wrapper.py          # Dingo算子集成
│   ├── unstructured_io_wrapper.py # UnstructuredIO集成
│   └── custom_operator_loader.py # 自定义算子加载器
└── requirements.txt              # Python依赖
```

### 算子市场架构
位置：`runtime/operators/`

```
算子仓库
├── README.md                     # 算子开发规范
├── examples/                     # 算子示例
│   └── text_length_filter/       # 文本长度过滤算子
│       ├── metadata.json         # 算子元数据
│       └── operator.py           # 算子实现
├── templates/                    # 算子模板
└── specifications/               # 算子规范定义
```

### DataX集成架构
位置：`runtime/datax/`

- **社区版**: 作为JAR依赖内置到执行引擎服务 
- **企业版**: 独立部署的DataX集群，通过API调用
- **配置**: 通过`DATAX_HOME`环境变量指定安装目录


## 部署架构设计

### 容器化部署
位置：`deployment/docker/` 和 `editions/*/docker/`

```
容器部署架构
├── api-gateway/                 # API网关容器
│   ├── Dockerfile
│   ├── nginx.conf              # 负载均衡配置
│   └── application.yml
│
├── main-application/           # 主应用容器
│   ├── Dockerfile
│   ├── application.yml
│   └── entrypoint.sh
│
├── frontend/                   # 前端容器
│   ├── console.Dockerfile
│   ├── annotation.Dockerfile
│   └── nginx.conf
│
└── infrastructure/             # 基础设施容器
    ├── mysql/
    ├── redis/
    ├── elasticsearch/
    └── minio/
```

### Kubernetes部署
位置：`deployment/kubernetes/` 和 `editions/*/k8s/`

```
K8s部署架构
├── namespaces/                 # 命名空间定义
├── configmaps/                 # 配置文件
├── secrets/                    # 密钥管理
├── services/                   # 服务定义
├── deployments/                # 部署定义
├── ingress/                    # 入口配置
├── persistent-volumes/         # 存储卷
└── monitoring/                 # 监控配置
```

## API规范架构

### OpenAPI 3.0规范
位置：`openapi/specs/`

```
API规范管理
├── data-management.yaml        # 数据管理API规范
├── data-collection.yaml        # 数据归集API规范
├── operator-market.yaml        # 算子市场API规范
├── data-cleaning.yaml          # 数据清洗API规范
├── data-synthesis.yaml         # 数据合成API规范
├── data-annotation.yaml        # 数据标注API规范
├── data-evaluation.yaml        # 数据评估API规范
├── pipeline-orchestration.yaml # 流程编排API规范
├── execution-engine.yaml       # 执行引擎API规范
└── rag-services.yaml           # RAG服务API规范
```

### 代码生成流程
位置：`scripts/build/generate-api.ps1`

API代码生成工作流
1. 读取OpenAPI YAML规范文件
2. 使用openapi-generator-maven-plugin生成:
   - 接口定义 (com.dataengine.*.interfaces.api)
   - DTO类 (com.dataengine.*.interfaces.dto)
   - 客户端SDK (可选)
3. 输出到各服务的target/generated-sources/
4. 集成到Maven编译流程
```
│                      运行时层 (Runtime)                          │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────────┐ │
│ │Python执行器 │ │   DataX     │ │      自定义算子库            │ │
│ │(Ray Worker) │ │   引擎      │ │    (Operators Library)      │ │
│ └─────────────┘ └─────────────┘ └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                    基础设施层 (Infrastructure)                   │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────────────────┐ │
│ │数据库   │ │消息队列 │ │对象存储 │ │       监控告警           │ │
│ │MySQL/PG │ │Redis/MQ │ │MinIO/S3 │ │   Prometheus/Grafana    │ │
│ └─────────┘ └─────────┘ └─────────┘ └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```


## 架构设计原则

### 1. 双微服务架构
- **API Gateway**: 独立微服务，处理路由、认证、限流
- **Main Application**: 独立微服务，聚合所有业务JAR包

### 2. JAR包依赖模式
- 各业务服务以JAR包形式提供
- 通过Spring Boot的@ComponentScan自动装配
- 保持模块化的同时避免过度的微服务拆分

### 3. API First设计
- 所有服务API通过OpenAPI 3.0规范定义
- 使用openapi-generator-maven-plugin生成接口和DTO
- 支持多语言客户端SDK生成

### 4. 组件全解耦
 - 核心业务模块解耦，能够支持独立拆分运行
 - 公共启动在main-application包含配置，模块独立配置由模块自己维护，通过config引入
## 监控与运维架构

### 监控体系设计
位置：`monitoring/` 和 `deployment/monitoring/`

```
监控架构
├── prometheus/                  # 指标收集
│   ├── prometheus.yml          # Prometheus配置
│   ├── rules/                  # 告警规则
│   └── targets/                # 监控目标
│
├── grafana/                    # 可视化监控
│   ├── dashboards/             # 仪表板
│   ├── datasources/            # 数据源配置
│   └── plugins/                # 插件配置
│
└── alerting/                   # 告警系统
    ├── alertmanager.yml        # 告警管理配置
    ├── webhooks/               # Webhook配置
    └── templates/              # 告警模板
```

### 日志管理架构

```
日志管理
├── 应用日志                     # Spring Boot应用日志
│   ├── api-gateway.log         # API网关日志
│   ├── main-application.log    # 主应用日志
│   └── service-*.log           # 各服务模块日志
│
├── 访问日志                     # Nginx/Gateway访问日志
│   ├── access.log              # HTTP访问日志
│   └── error.log               # 错误日志
│
└── 系统日志                     # 基础设施日志
    ├── mysql.log               # 数据库日志
    ├── redis.log               # 缓存日志
    └── elasticsearch.log       # 搜索引擎日志
```

## 测试架构设计

### 测试层次结构
位置：`tests/`

```
测试架构
├── unit/                       # 单元测试
│   ├── backend/                # 后端单元测试
│   │   ├── domain/             # 领域层测试
│   │   ├── application/        # 应用层测试
│   │   ├── infrastructure/     # 基础设施层测试
│   │   └── interfaces/         # 接口层测试
│   └── frontend/               # 前端单元测试
│       ├── components/         # 组件测试
│       └── utils/              # 工具函数测试
│
├── integration/                # 集成测试
│   ├── api/                    # API集成测试
│   ├── database/               # 数据库集成测试
│   ├── message-queue/          # 消息队列集成测试
│   └── external-services/      # 外部服务集成测试
│
├── e2e/                        # 端到端测试
│   ├── user-workflows/         # 用户工作流测试
│   ├── data-pipeline/          # 数据管道测试
│   └── admin-operations/       # 管理操作测试
│
└── performance/                # 性能测试
    ├── load-testing/           # 负载测试
    ├── stress-testing/         # 压力测试
    └── benchmark/              # 基准测试
```

## 构建与发布架构

### 构建脚本体系
位置：`scripts/build/`

```
构建脚本
├── build.sh / build.bat        # 主构建脚本
├── generate-api.ps1            # API代码生成脚本
├── docker-build.sh             # Docker镜像构建
├── frontend-build.sh           # 前端应用构建
└── package.sh                  # 应用打包脚本
```

### CI/CD流水线架构

```
CI/CD流水线
├── Source Code (Git)           # 源代码管理
│   ├── feature branches        # 功能分支
│   ├── develop branch          # 开发分支
│   └── main branch             # 主分支
│
├── Build Pipeline              # 构建流水线
│   ├── Code Quality Check      # 代码质量检查
│   ├── Unit Tests              # 单元测试
│   ├── API Generation          # API代码生成
│   ├── Maven Build             # Maven构建
│   ├── Frontend Build          # 前端构建
│   └── Docker Build            # 容器构建
│
├── Test Pipeline               # 测试流水线
│   ├── Integration Tests       # 集成测试
│   ├── E2E Tests               # 端到端测试
│   ├── Performance Tests       # 性能测试
│   └── Security Scan           # 安全扫描
│
└── Deploy Pipeline             # 部署流水线
    ├── Staging Deployment      # 预发布部署
    ├── Production Deployment   # 生产环境部署
    ├── Blue-Green Deployment   # 蓝绿部署
    └── Rollback Strategy       # 回滚策略
```

## 数据架构设计

### 数据存储架构

```
数据存储层
├── 关系型数据库 (MySQL/PostgreSQL)
│   ├── 用户管理数据             # 用户、角色、权限
│   ├── 业务元数据               # 数据源、数据集、血缘
│   ├── 流程编排数据             # 管道、任务、调度
│   └── 系统配置数据             # 系统参数、算子配置
│
├── 文档数据库 (Elasticsearch)
│   ├── 全文检索索引             # 文档内容、算子描述
│   ├── 日志数据索引             # 应用日志、操作日志
│   └── 指标数据索引             # 性能指标、业务指标
│
├── 缓存数据库 (Redis)
│   ├── 会话缓存                 # 用户会话、JWT Token
│   ├── 业务缓存                 # 热点数据、查询结果
│   └── 分布式锁                 # 任务锁、资源锁
│
└── 对象存储 (MinIO/S3)
    ├── 数据文件存储             # 原始数据文件
    ├── 模型文件存储             # 训练模型、算子包
    ├── 临时文件存储             # 处理中间文件
    └── 备份文件存储             # 数据备份、配置备份
```

### 数据流架构

```
数据流处理
├── 数据接入层
│   ├── REST API接入            # HTTP/HTTPS数据接入
│   ├── 文件上传接入            # 批量文件上传
│   ├── 数据库连接接入          # 关系型/NoSQL数据库
│   └── 消息队列接入            # Kafka/RabbitMQ消息
│
├── 数据处理层
│   ├── 流式处理引擎            # Ray
│   ├── 批处理引擎              # DataX
│   ├── 算子执行引擎            # Python Runtime
│   └── 模型推理引擎            # TensorFlow/PyTorch
│
├── 数据存储层
│   ├── 原始数据存储            # 未处理数据
│   ├── 清洗数据存储            # 清洗后数据
│   ├── 标注数据存储            # 标注结果数据
│   └── 模型数据存储            # 训练/推理数据
│
└── 数据服务层
    ├── 数据查询服务            # 数据检索、过滤
    ├── 数据导出服务            # 数据下载、同步
    ├── 数据血缘服务            # 血缘追踪、影响分析
    └── 数据质量服务            # 质量评估、报告
```

## 安全架构设计

### 安全防护体系

```
安全架构
├── 网络安全层
│   ├── API网关安全             # 限流、防DDoS、IP白名单
│   ├── HTTPS/TLS加密           # 传输层加密
│   ├── VPN接入                 # 企业网络接入
│   └── 防火墙策略              # 网络访问控制
│
├── 应用安全层
│   ├── 身份认证                # JWT、OAuth2、LDAP
│   ├── 权限控制                # RBAC、资源权限
│   ├── 数据加密                # 敏感数据加密存储
│   └── 审计日志                # 操作审计、访问日志
│
├── 数据安全层
│   ├── 数据脱敏                # 个人信息脱敏
│   ├── 数据备份                # 定期备份、异地存储
│   ├── 数据恢复                # 灾难恢复、快速恢复
│   └── 数据销毁                # 安全删除、彻底清理
│
└── 运维安全层
    ├── 容器安全                # 镜像扫描、运行时安全
    ├── 密钥管理                # Vault、密钥轮转
    ├── 漏洞扫描                # 代码扫描、依赖扫描
    └── 安全监控                # 异常检测、入侵检测
```


## OpenAPI代码生成

### Maven插件配置
每个JAR包服务都配置了openapi-generator-maven-plugin：

```xml
<plugin>
    <groupId>org.openapitools</groupId>
    <artifactId>openapi-generator-maven-plugin</artifactId>
    <version>6.6.0</version>
    <executions>
        <execution>
            <goals>
                <goal>generate</goal>
            </goals>
            <configuration>
                <inputSpec>${project.basedir}/../../../openapi/specs/${service-name}.yaml</inputSpec>
                <generatorName>spring</generatorName>
                <output>${project.build.directory}/generated-sources/openapi</output>
                <apiPackage>com.dataengine.${package}.interfaces.api</apiPackage>
                <modelPackage>com.dataengine.${package}.interfaces.dto</modelPackage>
                <configOptions>
                    <interfaceOnly>true</interfaceOnly>
                    <useTags>true</useTags>
                    <useSpringBoot3>true</useSpringBoot3>
                    <documentationProvider>springdoc</documentationProvider>
                </configOptions>
            </configuration>
        </execution>
    </executions>
</plugin>
```

### API规范文件
- 位置: `openapi/specs/`
- 包含所有服务的完整API定义
- 支持多版本管理

## 服务配置方式

### JAR包服务配置类
每个JAR包服务不再有`main`方法，而是通过配置类提供服务：

```java
@SpringBootApplication
@EnableFeignClients
@ComponentScan(basePackages = {
    "com.dataengine.annotation",
    "com.dataengine.shared"
})
public class DataAnnotationServiceConfiguration {
    // Service configuration class for JAR packaging
}
```

### 主应用聚合配置
Main Application通过依赖和ComponentScan聚合所有JAR包服务：

```java
@SpringBootApplication
@ComponentScan(basePackages = {
    "com.dataengine.datamanagement",
    "com.dataengine.collection",
    "com.dataengine.operator",
    "com.dataengine.cleaning",
    "com.dataengine.synthesis",
    "com.dataengine.annotation",
    "com.dataengine.evaluation",
    "com.dataengine.pipeline",
    "com.dataengine.execution",
    "com.dataengine.rag",
    "com.dataengine.shared"
})
public class MainApplication {
    public static void main(String[] args) {
        SpringApplication.run(MainApplication.class, args);
    }
}
```

## 服务间通信

### 内部通信
- JAR包服务之间：直接方法调用（同JVM）
- 通过Spring的依赖注入机制

### 外部通信
- 前端 → API Gateway → Main Application
- API Gateway通过HTTP转发到Main Application
- 支持gRPC（高性能场景）

### 异步通信
- 消息队列（Redis/RabbitMQ）
- 事件驱动架构
- Spring Events（JVM内部事件）

### 数据一致性
- 最终一致性
- Saga模式
- 本地事务（JAR包服务共享数据库）

## 部署架构

### 生产环境部署
1. **API Gateway**: 独立容器部署，负载均衡
2. **Main Application**: 独立容器部署，水平扩展
3. **数据库**: 主从复制，读写分离
4. **缓存**: Redis集群
5. **对象存储**: MinIO集群或云存储

### 开发环境部署
1. API Gateway: localhost:8080
2. Main Application: localhost:8090
3. 本地MySQL/Redis
4. 本地MinIO

## 优势与考虑

### 架构优势
1. **简化部署**: 只需要部署2个微服务
2. **降低复杂度**: 避免了分布式事务问题
3. **提高性能**: JVM内部调用，无网络开销
4. **便于开发**: 本地调试更容易
5. **API First**: 标准化的接口定义和代码生成

### 设计考虑
1. **可扩展性**: Main Application可以按需水平扩展
2. **模块化**: JAR包形式保持模块边界清晰
3. **测试友好**: 可以单独测试每个JAR包服务
4. **未来迁移**: 需要时可以轻松拆分为独立微服务
