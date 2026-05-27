## 1. Dependency and Configuration

- [x] 1.1 Add `sentry-sdk` to `requirements.txt`.
- [x] 1.2 Add Sentry SDK initialization to `netology_pd_diplom/settings.py` after `.env` loading.
- [x] 1.3 Configure the SDK with the project DSN and the requested `send_default_pii`, `enable_logs`, tracing, and profiling options.
- [x] 1.4 Document the Sentry DSN setting in `.env.example` if the project keeps the DSN in environment configuration.

## 2. Debug API Endpoint

- [x] 2.1 Add a `SentryDebugView` DRF `APIView` in `backend/views.py` with a GET handler that raises an unhandled exception.
- [x] 2.2 Ensure the debug view can be reached for manual verification despite the project's admin-only DRF default permissions.
- [x] 2.3 Register the slashless `/api/v1/sentry-debug` route in `backend/urls.py`.

## 3. Verification

- [x] 3.1 Run `python3 manage.py check` to verify Django configuration loads successfully.
- [x] 3.2 Start the application with a configured Sentry DSN and request `/api/v1/sentry-debug` to generate a test exception.
- [x] 3.3 Confirm the generated exception appears in Sentry with traceback context.
