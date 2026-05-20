# MAINTAIN.md — 版本迭代记录

**业务前缀**: `ap_`（数据库表、Redis Key、缓存键等统一使用此前缀）

## 版本规范

格式：`v{大}.{中}.{小}`

| 版本类型 | 触发条件 | 操作 |
|---|---|---|
| 大版本 | 用户通知大更新 | main 打 tag，记录重大变更 |
| 中版本 | 用户通知发布 | dev 合并到 main，打 tag |
| 小版本 | 每次提交自动 | 小版本 +1，自动 commit+push |

---

## v0.1.0 — 内容填充与 Cloudflare 部署（2026-05-20）

### 做什么
- 按 10 个编程语言分类填充工具/软件数据（Go/Rust/Java/Flutter/Vue/React/Python/PHP/C++/C#）
- 每个分类 10 个工具条目，共 100 个，含直链和版本信息
- 编写 seed_data.py 种子脚本，数据入库 SQLite
- 导出静态 data.json 供前端 fallback 读取
- 修改 Home.vue 支持 API 不可用时自动切换静态数据模式
- 部署到 Cloudflare Workers（apps-startpage.dabendi66.workers.dev）

### 为什么
- 需要为起始页填充实际的开发工具数据，覆盖主流编程语言生态
- Cloudflare Workers 部署实现零成本、全球 CDN 分发

### 怎么做
- 创建 feat/content-fill 分支开发
- 编写 seed_data.py（100 tools + 10 categories）直接写入 SQLite
- 导出 data.json 到 frontend/public/
- 修改 Home.vue 增加 isStaticMode + loadToolsFromStatic fallback
- 使用 wrangler + Workers Assets 部署静态站点

### 影响范围
- 新增：backend/seed_data.py、frontend/public/data.json、deploy/ 目录
- 修改：frontend/src/pages/Home.vue（静态数据 fallback）
- 部署：Cloudflare Workers (apps-startpage.dabendi66.workers.dev)

---

## v0.0.0 — 项目初始化（2026-04-28）

### 做什么
- 创建技术方案文档与开发计划
- 确定项目定位：个人应用起始页 / 工具集合入口 / 文件临时上传
- 确定技术栈：Python 3.12 + FastAPI + Vue 3 + Tailwind CSS + shadcn/ui
- 确定数据存储：SQLite（业务数据）
- 确定部署方式：Docker Compose 一键启动

### 为什么
- 需要一个统一的入口管理个人常用的开发工具、软件、文档、环境
- 跨平台环境下需要快速找到和下载所需工具
- 需要临时文件上传能力方便日常使用
- macOS 质感黑白灰风格符合审美需求

### 怎么做
- 编写完整技术方案文档
- 按 18 条规范要求设计架构
- 制定分阶段开发计划（PLAN.md）
