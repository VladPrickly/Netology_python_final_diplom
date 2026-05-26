# AGENTS.md

## Project Shape
- Django project package: `netology_pd_diplom`; the only real app is `backend`.
- API routes mount at `/api/v1/` from `backend/urls.py` and are mostly slashless, e.g. `/api/v1/user/login`; Swagger UI is `/schema/swagger-ui/`, ReDoc is `/schema/redoc/`, schema is `/schema`.
- Main wiring lives in `backend/models.py`, `backend/serializers.py`, `backend/views.py`, and async work in `backend/tasks.py`.
- `README.md` and `docs_reference/` are legacy Netology/reference docs; trust executable config and current source when they disagree.

## Commands
- Install deps with `python3 -m pip install -r requirements.txt`.
- Settings require a local `.env` loaded by `python-dotenv`; `.env.example` documents required keys and there is no active sqlite fallback in `settings.py`.
- Docker path: `docker compose up --build` starts Postgres, Redis, app, Celery, and Flower; the app command runs `python manage.py migrate` before `runserver`.
- Non-Docker path: run Postgres and Redis yourself, then `python3 manage.py migrate` and `python3 manage.py runserver 0.0.0.0:8000`.
- Celery worker command from compose: `celery -A netology_pd_diplom worker --loglevel=info --logfile=celery.log`; Flower listens on port `5555`.

## Verification
- No pytest, lint, formatter, typecheck, pre-commit, or CI config is committed; use Django checks/tests.
- Quick smoke check: `python3 manage.py check`.
- Full tests: `python3 manage.py test`.
- App tests: `python3 manage.py test backend`.
- Single throttling test example: `python3 manage.py test backend.tests.test_throttling.AuthThrottlingTestCase.test_register_account_throttling`.

## Repo Gotchas
- Requirements pin Django 5.2.x and Docker uses Python 3.12; ignore stale Django 2.2 comments in generated files.
- `AUTH_USER_MODEL` is `backend.User` with email as `USERNAME_FIELD`; `username` still exists but is not unique, so create users/superusers through email-first flows.
- `DEBUG = os.getenv('DEBUG')` is a raw string, so `DEBUG=False` in `.env` is still truthy unless settings are fixed.
- DRF default permissions are `IsAdminUser`; endpoints without explicit `permission_classes` are admin-only before manual `request.user` checks run.
- Token auth/session auth are configured; `simplejwt` is installed but not wired in `REST_FRAMEWORK`.
- Registration, order confirmation, and partner import call Celery `.delay()`; run Redis plus a worker for those flows.
- Partner import (`POST /api/v1/partner/update`) fetches YAML from a URL, requires an authenticated `shop` user, and expects `shop`, `categories`, and `goods` keys like `data/shop*.yaml`.
- Basket `POST`/`PUT` expect an `items` form field containing a JSON string; basket/contact `DELETE` expect comma-separated IDs in `items`.
- New migration files are ignored by `.gitignore` via `*/migrations/*`; only `backend/migrations/__init__.py` is committed, so decide explicitly how migrations should be tracked when models change.
- `SOCIAL_AUTH_PIPELINE` references `backend.pipeline.*`, but no `backend/pipeline.py` is present in this repo.
