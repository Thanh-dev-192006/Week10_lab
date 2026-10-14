# Hero API — Week 9 reference solution

Reference solution for the Week 9 lab ([labs/week09.md](../../../labs/week09.md)): a FastAPI + SQLModel API backed by PostgreSQL, with teams, heroes, missions (many-to-many), a seed script and Alembic migrations.

It is the **starting point for Week 10** (REST design, docs, CORS, `pytest` + `TestClient`).

## Structure

```
hero-api/
├── app/
│   ├── __init__.py
│   ├── database.py     # engine, get_session, SessionDep
│   ├── models.py       # tables (Team, Hero, Mission, HeroMissionLink) + API schemas
│   ├── main.py         # FastAPI app and endpoints
│   └── seed.py         # sample data: python -m app.seed
├── migrations/
│   ├── env.py          # reads DATABASE_URL, target_metadata = SQLModel.metadata
│   ├── script.py.mako  # + import sqlmodel
│   └── versions/
│       ├── a608522faa5d_initial_schema.py
│       └── 561a9fefd664_add_hero_power.py
├── alembic.ini
├── requirements.txt
├── answers.md          # answers to the lab questions
└── .env.example
```

## Run it

```bash
python -m venv .venv
source .venv/bin/activate              # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# PostgreSQL (user/db created as in Part 0 of the lab)
export DATABASE_URL="postgresql+psycopg://app:secret@localhost:5432/appdb"
# ...or leave it unset to use SQLite (./app.db)

alembic upgrade head                   # create the schema
python -m app.seed                     # sample data (safe to run twice)
fastapi dev app/main.py                # http://127.0.0.1:8000/docs
```

Starting from a database whose tables were created by `create_all` (Parts 4–8 of the lab)? Either drop them first, or mark the database as up to date with `alembic stamp head`.

## Endpoints

| Method & path | Body | Response | Status |
|---|---|---|---|
| `POST /heroes` | `HeroCreate` | `HeroPublic` | `201`, `404` unknown team |
| `GET /heroes?offset&limit&min_age&team_id&name` | — | `list[HeroPublic]` | `200`, `422` if `limit > 100` |
| `GET /heroes/{hero_id}` | — | `HeroPublic` | `200`, `404` |
| `PATCH /heroes/{hero_id}` | `HeroUpdate` | `HeroPublic` | `200`, `404` |
| `DELETE /heroes/{hero_id}` | — | — | `204`, `404` |
| `POST /teams` | `TeamCreate` | `TeamPublic` | `201`, `409` duplicate name |
| `GET /teams` | — | `list[TeamPublic]` | `200` |
| `GET /teams/{team_id}/heroes` | — | `list[HeroPublic]` | `200`, `404` |
| `POST /missions` | `MissionCreate` | `MissionPublic` | `201` |
| `POST /heroes/{hero_id}/missions/{mission_id}` | — | — | `204`, `404` |
| `GET /heroes/{hero_id}/missions` | — | `list[MissionPublic]` | `200`, `404` |

`secret_name` is stored in the database but never returned (`response_model=HeroPublic`).

## Week 10 additions

The project includes a working browser dashboard in `app/frontend`, status
filtering/updating, and automated API tests for CRUD, validation, CORS, teams,
and missions. Start the API with `fastapi dev app/main.py`, then serve the
frontend in another terminal with `python -m http.server 5500 --directory app/frontend`.

Open `http://localhost:5500` for the dashboard or `http://127.0.0.1:8000/docs`
for the interactive OpenAPI documentation. Run tests with `pytest -q`.

## Notes for Week 10

- `get_session` in `app/database.py` is the dependency to **override** in tests (`app.dependency_overrides[get_session] = ...`) with an in-memory SQLite engine (`StaticPool`).
- The lifespan in `app/main.py` still calls `create_all`; with Alembic in place that is only a development convenience.
- Any model change (e.g. Week 10's `status` and `created_at`) needs a new migration: `alembic revision --autogenerate -m "..."`, review it, `alembic upgrade head`.
