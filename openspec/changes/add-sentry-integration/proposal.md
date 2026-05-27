## Why

Production-like Django projects need centralized visibility into runtime errors so regressions can be investigated with full traceback context. Adding a basic Sentry integration and a deliberate debug endpoint gives the project a simple way to verify that error capture is wired correctly.

## What Changes

- Add Sentry SDK initialization to the Django settings so unhandled errors are reported to Sentry.
- Add configuration for the provided Sentry DSN and basic SDK options, including default PII, logs, tracing, and profiling settings.
- Add a DRF `APIView` endpoint that deliberately raises an exception for manual Sentry verification.
- Expose the debug endpoint through the existing API URL routing.
- Add `sentry-sdk` to Python dependencies.

## Capabilities

### New Capabilities

- `sentry-error-monitoring`: Covers configuring Sentry for the Django application and exposing a debug API endpoint that triggers a captured exception.

### Modified Capabilities

- None.

## Impact

- Affects Django settings in `netology_pd_diplom/settings.py`.
- Affects backend API routing and views in `backend/views.py` and `backend/urls.py`.
- Adds a runtime dependency in `requirements.txt`.
- Introduces an intentionally failing endpoint for manual verification in local development.
