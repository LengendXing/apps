# PLAN.md — 开发计划

**当前版本**: `v0.0.0` → 目标 `v0.1.0`（MVP）
**当前分支**: `dev`
**业务前缀**: `ap_`

---

## 已完成

- [x] 技术方案设计
- [x] MAINTAIN.md 创建
- [x] PLAN.md 创建

## 待完成 — Phase 1：项目骨架

- [ ] P1-1 初始化 Git 仓库，创建 dev 分支，推送至 GitHub
- [ ] P1-2 创建 `.gitignore`、`.env.example`
- [ ] P1-3 初始化后端项目（FastAPI + pyproject.toml）
- [ ] P1-4 初始化前端项目（Vue 3 + Vite + TypeScript + Tailwind + shadcn/ui）
- [ ] P1-5 创建 Dockerfile + docker-compose.yml
- [ ] P1-6 创建目录结构

## 待完成 — Phase 2：后端基础设施

- [ ] P2-1 配置管理（config.py），读取 .env，版本常量维护
- [ ] P2-2 SQLite 连接层（aiosqlite + SQLAlchemy 异步引擎）
- [ ] P2-3 Alembic 初始化，创建首条迁移
- [ ] P2-4 统一响应格式 `{code, message, data}` + 错误码规范
- [ ] P2-5 结构化日志中间件
- [ ] P2-6 JWT 认证中间件
- [ ] P2-7 输入校验层（pydantic model 验证）

## 待完成 — Phase 3：核心 API

- [ ] P3-1 用户认证（注册/登录/Token 管理）
- [ ] P3-2 工具分类 CRUD（ap_categories）
- [ ] P3-3 工具条目 CRUD（ap_tools）
- [ ] P3-4 文件上传接口（临时文件，支持预览）
- [ ] P3-5 审计日志查询接口

## 待完成 — Phase 4：前端起始页

- [ ] P4-1 前端项目配置（Tailwind 黑白灰主题、日夜切换）
- [ ] P4-2 Layout 布局（顶栏 + 内容区）
- [ ] P4-3 i18n 初始化（vue-i18n，中/英文）
- [ ] P4-4 登录页面
- [ ] P4-5 起始页 — 工具分类卡片 + 搜索
- [ ] P4-6 工具详情/编辑页
- [ ] P4-7 临时文件上传组件
- [ ] P4-8 统一 API 请求层 + toast 错误提示

## 待完成 — Phase 5：规范与质量

- [ ] P5-1 三套环境配置
- [ ] P5-2 后端测试覆盖率 ≥ 80%
- [ ] P5-3 前端 lint + build 通过
- [ ] P5-4 依赖安全扫描
- [ ] P5-5 Docker Compose 一键启动验证
- [ ] P5-6 README 完善

## 待完成 — Phase 6：发布

- [ ] P6-1 feat 分支合并回 dev
- [ ] P6-2 dev 合并到 main，打 tag `v0.1.0`
- [ ] P6-3 切回 dev 分支
- [ ] P6-4 更新 MAINTAIN.md 记录 v0.1.0 发布内容

---

## 技术栈

| 层 | 技术 |
|---|---|
| 后端 | Python 3.12 + FastAPI + SQLAlchemy + Alembic |
| 前端 | Vue 3 + Vite + TypeScript + Tailwind CSS + shadcn/ui |
| 存储 | SQLite（业务数据） |
| 认证 | JWT + passlib bcrypt |
| 部署 | Docker Compose |
| i18n | vue-i18n |

## 数据存储

| 表 | 用途 |
|---|---|
| `ap_users` | 用户 |
| `ap_categories` | 工具分类 |
| `ap_tools` | 工具条目（名称、描述、链接、分类、平台标签） |
| `ap_file_uploads` | 临时文件记录 |
| `ap_audit_logs` | 审计日志 |

## 分支策略

```
main (生产) ← dev (开发) ← feat/任务名
```

## 技术方案

### 项目定位
个人应用起始页 — 统一管理常用开发工具、软件、文档、环境的入口。支持快速搜索、分类浏览、文件临时上传。

### UI 风格
- macOS 质感：磨砂玻璃、柔和阴影、圆角、微妙动画
- 黑白灰三色主题，不支持其他颜色
- 白天/夜间双模式，切换按钮在顶栏右上角
- Tailwind CSS + shadcn/ui 组件库

### 核心功能
1. **工具集合页**：按分类展示开发工具卡片，支持搜索过滤
2. **工具管理**：后台管理，CRUD 工具条目
3. **临时文件上传**：快速上传、预览、自动过期清理
4. **审计日志**：关键操作记录
