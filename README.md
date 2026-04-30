<div align="center">

# 🧠 LLM Wiki Team

**面向团队协作的智能知识管理系统**

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg?style=flat-square)](./LICENSE)
[![GitHub Issues](https://img.shields.io/github/issues/:owner/:repo/issues?style=flat-square)](https://github.com/:owner/:repo/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)

</div>

---

## 📖 Introduction

**LLM Wiki Team** 是一个支持团队协作、基于 LLM-Wiki 方法论的知识管理系统。它将可视化知识管理、LLM 驱动的知识问答与 Agent 共享记忆融为一体，为团队提供：

- 🗂️ **可视化知识管理** — 多空间、多层级的知识库组织与 Markdown 协作编辑
- 🤖 **LLM 知识问答** — 基于项目知识库的智能问答、深度研究与流式对话
- 🧩 **Agent 共享记忆** — 为团队成员使用的 AI Agent 提供共享的长期项目记忆和团队记忆
- 🔗 **知识图谱** — 知识节点之间的关联、追溯与可视化导航

---

## 🙏 致谢与知识产权声明

本项目主要参考并借鉴了以下两个优秀的开源项目，我们对原作者的创造性工作表示最诚挚的敬意和感谢：

### [MM-Wiki](https://github.com/phachon/mm-wiki)

> 作者：[phachon](https://github.com/phachon) | 协议：[MIT License](https://github.com/phachon/mm-wiki/blob/master/LICENSE)

MM-Wiki 是一个轻量级的企业知识分享与团队协同软件。本项目在以下方面参考了 MM-Wiki 的设计：

- **Web 前端架构** — 多空间知识库的 UI 交互与布局设计
- **团队协作功能** — 用户角色、权限管理、空间隔离等协作机制
- **知识库管理** — 文档树形组织、Markdown 编辑与预览、全文搜索
- **系统架构** — Go 后端与前端模板的整体架构设计

### [LLM Wiki Lite](https://github.com/Akers/llm_wiki_lite)

LLM Wiki Lite 是基于[llm_wiki](https://github.com/nashsu/llm_wiki)的知识管理后端服务。

> llm_wiki作者：[Yong Su (nashsu)](https://github.com/nashsu) | 协议：[GPLv3](https://github.com/nashsu/llm_wiki_lite/blob/master/LICENSE)

本项目深度集成LLM Wiki Lite作为知识图谱管理引擎，并在以下方面集成并借鉴了 LLM Wiki：

- **知识摄取管道** — 双步链式思考（Two-Step CoT）文档摄取与 Wiki 生成
- **混合搜索引擎** — 分词搜索 + 向量语义搜索 + RRF 融合排序
- **LLM 集成** — 多 LLM 提供商适配（OpenAI / Anthropic / Google / Ollama 等）
- **深度研究** — 自动搜索、综合与知识沉淀的 Deep Research 流程
- **Rust 后端服务** — 作为核心知识图谱引擎的子模块深度集成

---

> ⚠️ **知识产权承诺**：本项目严格遵守上述两个项目的开源协议。由于本项目深度集成了 LLM Wiki Lite 的代码（GPLv3），因此本项目整体采用 **GNU General Public License v3.0** 开源协议。MM-Wiki 的 MIT 协议代码在 GPLv3 下使用完全合规。我们承诺持续尊重并保护原作者的知识产权，所有衍生作品均保持开源。

---

<details open>
<summary>
 ✨ Features
</summary> <br />

### 知识管理

- 📁 多空间知识库，支持团队/部门级别隔离
- 📝 Markdown 编辑器，支持实时预览
- 🌳 树形文档结构，拖拽排序
- 🔍 全文搜索 + 语义搜索
- 📎 文档附件管理与版本追溯

### LLM 智能能力

- 💬 基于知识库的智能问答（SSE 流式输出）
- 🔬 深度研究模式（自动搜索 → 综合整理 → 知识沉淀）
- 📥 多格式文档摄取（PDF / DOCX / PPTX / XLSX / 网页剪藏）
- 🧠 双步链式思考知识提取

### 团队协作

- 👥 用户角色与细粒度权限管理
- 🔔 文档变更通知
- 📊 活动日志与审计

### Agent 记忆共享

- 🤖 为 AI Agent 提供项目级长期记忆接口
- 🧠 团队共享知识池，Agent 可读写
- 🔌 MCP（Model Context Protocol）标准接口

### 部署运维

- 🐳 Docker / Docker Compose 一键部署
- ☸️ Kubernetes 编排支持
- 🏗️ 前后端分离架构

</details>

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Frontend (Web UI)                  │
│         空间管理 │ 文档编辑 │ 知识图谱可视化          │
└──────────────────────┬──────────────────────────────┘
                       │ REST API / WebSocket
┌──────────────────────┴──────────────────────────────┐
│                  Backend API (Go)                     │
│    用户认证 │ 权限管理 │ 空间管理 │ Agent 记忆接口     │
└──────────┬───────────────────────────┬───────────────┘
           │                           │
┌──────────┴──────────┐   ┌───────────┴───────────────┐
│   Knowledge Engine  │   │      Database / Cache      │
│   (Rust / LLM Wiki  │   │  MySQL │ Redis │ LanceDB   │
│     Lite 集成)       │   └───────────────────────────┘
│  摄取 │ 搜索 │ 聊天  │
│  深度研究 │ 向量化    │
└─────────────────────┘
```

---

## 📁 Project Structure

```
llm_wiki_team/
├── frontend/              # Web 前端
│   └── ...                # (待规划)
├── backend/               # Go 后端 API 服务
│   ├── api/               # HTTP 路由与处理器
│   ├── core/              # 核心业务逻辑
│   ├── models/            # 数据模型
│   └── services/          # 业务服务层
├── config/                # 配置文件模板
├── deploy/                # 部署配置
│   ├── docker/            # Docker 相关文件
│   └── k8s/               # Kubernetes 编排
├── docs/                  # 项目文档
├── scripts/               # 构建/运维脚本
├── LICENSE                # GPLv3 开源协议
└── README.md              # 项目说明
```

---

## 🚀 Quick Start

> 🚧 **注意**：本项目处于早期规划阶段，以下为计划的快速启动流程。

### Prerequisites

- Docker & Docker Compose
- Go 1.21+
- Node.js 18+ (前端开发)
- Rust 1.75+ (知识引擎开发)

### Using Docker Compose (Recommended)

```bash
# 克隆仓库
git clone https://github.com/:owner/:repo.git
cd llm_wiki_team

# 使用 Docker Compose 启动所有服务
docker compose -f deploy/docker/docker-compose.yml up -d
```

### Development Setup

```bash
# 1. 启动依赖服务（MySQL、Redis 等）
docker compose -f deploy/docker/docker-compose.dev.yml up -d

# 2. 启动后端 API
cd backend
go run main.go

# 3. 启动前端开发服务器
cd frontend
npm install
npm run dev
```

---

## 🛠️ Tech Stack

| 层级 | 技术 | 说明 |
|------|------|------|
| **前端** | React / Vue | Web UI（待定） |
| **后端 API** | Go + Gin/Echo | 团队协作与权限管理 |
| **知识引擎** | Rust + Actix Web | LLM Wiki Lite 深度集成 |
| **数据库** | MySQL | 用户、空间、文档元数据 |
| **缓存** | Redis | Session、热点缓存 |
| **向量存储** | LanceDB | 语义搜索向量索引 |
| **LLM** | OpenAI / Anthropic / Ollama | 多提供商适配 |
| **部署** | Docker / K8s | 容器化部署 |

---

## 🗺️ Roadmap

- [ ] **Phase 1: 基础框架** — 项目脚手架、数据库设计、基础 API
- [ ] **Phase 2: 知识管理** — 空间/文档 CRUD、Markdown 编辑器、权限系统
- [ ] **Phase 3: LLM 集成** — 知识摄取管道、混合搜索、流式问答
- [ ] **Phase 4: Agent 记忆** — Agent 长期记忆接口、团队共享记忆池
- [ ] **Phase 5: 知识图谱** — 知识节点关联、图谱可视化
- [ ] **Phase 6: 部署优化** — Docker 镜像、K8s 编排、CI/CD

---

## 🤝 Contributing

我们欢迎并感谢所有形式的贡献！无论是 Bug 报告、功能建议、代码贡献还是文档改进。

在提交贡献之前，请阅读 [贡献指南](./CONTRIBUTING.md)。

### 贡献方式

- 🐛 **Bug 报告**：[提交 Issue](https://github.com/:owner/:repo/issues/new?template=bug_report.md)
- ✨ **功能建议**：[提交 Feature Request](https://github.com/:owner/:repo/issues/new?template=feature_request.md)
- 📖 **文档改进**：直接提交 PR
- 💻 **代码贡献**：Fork → Branch → PR

---

## 📄 License

本项目基于 [GNU General Public License v3.0](./LICENSE) 开源协议发布。

### 协议兼容性说明

| 参考项目 | 原协议 | 本项目使用方式 | 兼容性 |
|----------|--------|----------------|--------|
| [MM-Wiki](https://github.com/phachon/mm-wiki) | MIT License | 参考前端设计与协作功能 | ✅ MIT 代码可在 GPLv3 下使用 |
| [LLM Wiki Lite](https://github.com/nashsu/llm_wiki_lite) | GPLv3 | 深度集成（子模块） | ✅ GPLv3 ↔ GPLv3 完全兼容 |

---

## 📬 Contact

- **项目主页**：https://github.com/:owner/:repo
- **问题反馈**：[GitHub Issues](https://github.com/:owner/:repo/issues)

---

<div align="center">

**Built with ❤️ by the community, inspired by [MM-Wiki](https://github.com/phachon/mm-wiki) and [LLM Wiki Lite](https://github.com/nashsu/llm_wiki_lite)**

</div>
