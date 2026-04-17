# Architecture overview

## Frontend
- React + TypeScript SPA built with Vite
- Tailwind CSS for styling
- Route-based UI with a focused practice experience
- Stateless client: answers are never computed in the browser

## Backend
- FastAPI API with modular routers
- Question generation and validation in Python services
- Signed validation tokens prevent answer leakage
- Optional PostgreSQL persistence for sessions and attempts

## Persistence
- Practice sessions and question attempts are stored in PostgreSQL when enabled
- The app still runs without a database for lightweight local development

## Security basics
- HMAC-signed question payloads
- Input validation with Pydantic
- CORS controls
- Structured logging
