# Backend — FastAPI

Follows the structure of github.com/fastapi/full-stack-fastapi-template.

## Stack

- Python + FastAPI + SQLModel + PostgreSQL
- Alembic for migrations
- Redis for seat locking
- uv as package manager

## Commands

```bash
uv run fastapi dev                                          # dev server with hot reload on :8000
uv run alembic upgrade head                                 # apply migrations
uv run alembic revision --autogenerate -m "description"     # generate migration
uv run pytest                                               # run tests
```

## Project layout

```
backend/
├── app/
│   ├── main.py           # app entrypoint, router registration
│   ├── models.py         # ALL SQLModel models in a single file
│   ├── crud.py           # database operations by domain
│   ├── api/
│   │   ├── deps.py       # SessionDep, get_current_user, require_admin
│   │   └── routes/       # one file per domain router
│   └── core/
│       ├── config.py     # Settings via pydantic-settings
│       ├── db.py         # engine + init_db (creates first superuser)
│       └── security.py   # JWT creation/validation, password hashing
└── alembic/              # migrations
```

## Conventions

- All models in `app/models.py` — never split across files (SQLModel relationship requirement)
- Database operations go in `crud.py`, not inside route handlers
- Use `SessionDep` from `api/deps.py` for DB session injection in all routes
- Never use `SQLModel.metadata.create_all` in production — use Alembic only
- Route protection: `Depends(get_current_user)` for auth, `Depends(get_current_active_superuser)` for admin
- User access control via `is_superuser: bool` — no role enum

## Seat locking rules — critical

- Lock key: `seat-lock:{sessionId}:{seatId}` — TTL 300s
- Always use `SET NX EX` — never `SET` without `NX` (would overwrite another user's lock)
- If any seat fails to lock, release ALL partial locks before returning 409
- APScheduler job runs every minute to reset orphaned `locked` SessionSeats

## Environment variables

See `../.env.example` (project root) — copy to `../.env` and fill in the values before running.