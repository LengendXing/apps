# Apps Startpage

个人应用起始页 — 统一管理常用开发工具、软件、文档、环境的入口。

## Tech Stack

- **Backend**: Python 3.12 + FastAPI + SQLAlchemy
- **Frontend**: Vue 3 + Vite + TypeScript + Tailwind CSS
- **Storage**: SQLite
- **Auth**: JWT
- **Deploy**: Docker Compose

## Quick Start

```bash
# Backend
cd backend
pip install -e .
cp ../.env.development .env
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## Deploy with Docker

```bash
cp .env.example .env
docker compose up --build -d
```

## API

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check |
| POST | /api/auth/register | Register |
| POST | /api/auth/login | Login |
| GET | /api/categories | List tool categories |
| GET | /api/tools | List tools |
| POST | /api/tools | Create tool |
| POST | /api/uploads | Upload file |
| GET | /api/uploads | List uploads |
