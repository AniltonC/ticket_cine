# Ticket Cine

Cinema seat reservation system. Study project for fullstack web development.

## Structure

- `backend/` — FastAPI (Python)
- `frontend/` — Next.js (TypeScript)
- `docker-compose.yml` — PostgreSQL 16 + Redis 7

## Starting the environment

```bash
docker compose up -d                              # start PostgreSQL and Redis
cd backend && uv run fastapi dev app/main.py      # API on http://localhost:8000
cd frontend && npm run dev                        # frontend on http://localhost:3000
```

> Environment variables: see `.env.example` (project root)

## Architecture docs

Full architecture: [`docs/architecture.md`](docs/architecture.md)

Key decisions:
- Backend follows fastapi/full-stack-fastapi-template structure
- All SQLModel models live in a single `app/models.py` (required to avoid circular imports with SQLModel relationships)
- Database operations go in `crud.py`, never inside route handlers
- `SessionSeat` is the central entity for seat availability — generated automatically for every `Seat` when a `Session` is created
- Seat locking uses Redis `SET NX EX 300` — atomic, 5-minute TTL; key format: `seat-lock:{sessionId}:{seatId}`
- If `SET NX` fails for any seat, all locks acquired in the same request must be released before returning 409
- APScheduler job runs every minute to reset orphaned `locked` SessionSeats whose Redis key has expired
- JWT stored in httpOnly cookie on the frontend; payload contains only `sub` (user UUID as string)
- Password hashing: `pwdlib` with Argon2 (primary) + bcrypt (legacy fallback) — matches template
- JWT signing: `PyJWT` (`pyjwt`) with HS256 — matches template; do NOT use `python-jose`
- User model uses `is_superuser: bool` and `is_active: bool` — no role enum (matches template)
- `UserRegister` is the public signup schema; `UserCreate` is used internally by admins and can set `is_superuser=True`
- `UserPublic` does not expose `is_superuser` or `hashed_password`
- Route protection via `Depends(get_current_user)` for auth and `Depends(get_current_active_superuser)` for admin-only routes
- TMDB API is used only by admins to import movies; local `Movie` record becomes the source of truth after import