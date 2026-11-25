# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Bookmark Vault: a FastAPI + SQLModel API backed by SQLite. Early stage: only a `/health` route exists, and no table models are defined yet.

## Commands

The virtualenv is at `.venv` (Python 3.9). Use its binaries directly, or activate it first.

```bash
.venv/bin/pip install -r requirements.txt     # install deps (uvicorn is not listed; install it separately)
.venv/bin/uvicorn app.main:app --reload       # dev server on http://127.0.0.1:8000 (docs at /docs)
.venv/bin/pytest                              # all tests
.venv/bin/pytest tests/test_health.py::test_health   # single test
```

No linter or formatter is configured.

## Architecture

- `app/db.py` holds the single SQLAlchemy engine (`sqlite:///./bookmark_vault.db`, a path relative to the working directory). `get_session()` is a generator meant for use as a FastAPI dependency (`Depends(get_session)`).
- `app/models.py` is where SQLModel table models (`table=True`) go. `app/main.py` imports `app.models` only for its side effect: registering the tables on `SQLModel.metadata`. A model defined in a module that `main.py` doesn't import (directly or through `app.models`) won't get a table.
- Tables are created by `init_db()` (`SQLModel.metadata.create_all`) in the FastAPI `lifespan` hook at startup. There are no migrations. `create_all` creates only missing tables and never alters existing ones, so after a schema change, delete `bookmark_vault.db` (or add migrations).
- Tests use a module-level `TestClient(app)` without a `with` block, so the lifespan hook (and `init_db`) does **not** run in tests. Tests that touch the database need to either use `with TestClient(app) as client:` or override `get_session` via `app.dependency_overrides` with a separate test engine, so they don't write to the dev `bookmark_vault.db`.

## Python 3.9 constraint

The venv runs Python 3.9, so `X | None` union syntax isn't allowed in annotations that Pydantic or SQLModel evaluate at runtime. Use `Optional[X]` / `Union[...]` from `typing`.
