<<<<<<< HEAD
# Math Learning Platform

A production-ready math practice website with:

- **Integer operations** using positive and negative numbers
- **Algebraic expressions**
- **Algebra formulas / identities**

## Stack

- **Frontend:** React, TypeScript, Vite, Tailwind CSS
- **Backend:** FastAPI, SQLAlchemy, PostgreSQL-ready persistence
- **Validation:** Python services with stateless signed question tokens
- **Testing:** Vitest + React Testing Library, Pytest
- **Docker:** Local development stack with Postgres
- **Deployment:** Netlify frontend + Render backend

## Folder structure

```text
math-learning-platform/
├── apps/
│   ├── frontend/
│   └── backend/
├── infrastructure/
│   ├── docker/
│   ├── netlify/
│   └── render/
├── docs/
├── docker-compose.yml
└── README.md
```

A full detailed folder tree is also available in [`docs/folder-structure.txt`](docs/folder-structure.txt).

## Quick start

### Option 1: local without Docker

#### Frontend

```bash
cd apps/frontend
cp .env.example .env
npm install
npm run dev
```

#### Backend

```bash
cd apps/backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env
uvicorn app.main:app --reload
```

The frontend runs at `http://localhost:5173` and the backend at `http://localhost:8000`.

> The backend works without a database if `SESSION_PERSISTENCE_ENABLED=false`.  
> For persistent session history, use PostgreSQL and set `SESSION_PERSISTENCE_ENABLED=true`.

### Option 2: Docker with PostgreSQL

```bash
docker compose up --build
```

Services:

- Frontend: `http://localhost:4173`
- Backend: `http://localhost:8000`
- PostgreSQL: `localhost:5432`

## Environment variables

### Frontend (`apps/frontend/.env`)

```env
VITE_API_BASE_URL=http://localhost:8000
```

### Backend (`apps/backend/.env`)

```env
APP_NAME=Math Learning Platform API
APP_ENV=development
LOG_LEVEL=INFO
API_V1_PREFIX=/api/v1
BACKEND_CORS_ORIGINS=http://localhost:5173,http://localhost:4173,http://localhost:3000
QUESTION_TOKEN_SECRET=change-me
SESSION_PERSISTENCE_ENABLED=false
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/math_learning
```

## Tests

### Frontend

```bash
cd apps/frontend
npm install
npm run test
```

### Backend

```bash
cd apps/backend
pip install -e ".[dev]"
pytest
```

## Deployment

### Netlify frontend

- Base directory: `apps/frontend`
- Build command: `npm run build`
- Publish directory: `dist`
- Environment variable:
  - `VITE_API_BASE_URL=https://<your-render-service>.onrender.com`

### Render backend

- Root directory: `apps/backend`
- Build command: `pip install -e ".[dev]" && alembic upgrade head`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Add a managed PostgreSQL database and set:
  - `DATABASE_URL`
  - `QUESTION_TOKEN_SECRET`
  - `SESSION_PERSISTENCE_ENABLED=true`
  - `BACKEND_CORS_ORIGINS=https://<your-netlify-site>.netlify.app`

## Features

- 3 switchable learning modules
- Easy, medium, hard difficulty
- Dynamic question generation in Python
- Secure answer validation without exposing answers to the frontend
- Session scoring and attempt persistence
- Responsive UI
- Unit and integration test scaffolding
- Dockerized local stack
- Ready for Netlify + Render deployment

## Next steps for future production growth

- Authentication and per-user accounts
- Long-term analytics dashboards
- Teacher/admin tooling
- Saved progress and leaderboards
- Content moderation and question auditing
=======
# math-learn
>>>>>>> 90c01339ae804cd36384370d67d695d4e5a1e78f
