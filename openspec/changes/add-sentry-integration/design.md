## Context

The project is a Django 5.2 application with a single `backend` app and DRF routes mounted under `/api/v1/`. Settings already load environment variables from `.env`, and API views are centralized in `backend/views.py` with routes in `backend/urls.py`.

The change adds a new external monitoring dependency and a deliberate error endpoint so developers can verify that Django exceptions reach Sentry.

## Goals / Non-Goals

**Goals:**

- Initialize the official Sentry Python SDK during Django settings load.
- Configure the SDK with the provided Sentry DSN and requested baseline options for PII, logs, tracing, and profiling.
- Add a DRF `APIView` endpoint that raises an unhandled exception for manual verification.
- Keep routing consistent with the existing slashless `/api/v1/` API style.

**Non-Goals:**

- Add custom Sentry middleware, custom event processors, or alerting rules.
- Build a UI for Sentry status or event browsing.
- Change global error handling behavior beyond Sentry capture.
- Fix unrelated settings issues such as the current raw-string `DEBUG` parsing.

## Decisions

- Use `sentry-sdk` directly in `netology_pd_diplom/settings.py` after `.env` loading.
  - Rationale: Sentry's Django integration is auto-enabled by the SDK for Django apps, so no custom middleware or app registration is needed for the base integration.
  - Alternative considered: Add explicit integration classes and custom middleware. This is unnecessary for the requested baseline setup.

- Store the DSN in settings via environment configuration, with the provided DSN used for the project setup.
  - Rationale: The project already reads deployment-specific values from `.env`, and keeping the DSN configurable avoids baking environment-specific monitoring into code.
  - Alternative considered: Hardcode the DSN directly in `settings.py`. This matches the quickstart snippet but is less flexible for local or future deployments.

- Add a `SentryDebugView` APIView in `backend/views.py` and route it from `backend/urls.py` as `sentry-debug`.
  - Rationale: Existing project endpoints are DRF views under `/api/v1/`, and the task specifically asks for an APIView that raises an exception.
  - Alternative considered: Add a function route at the project URL level. That matches Sentry's quickstart example but would not follow the requested APIView approach or existing API routing style.

- Allow unauthenticated access to the debug view only as needed for manual verification.
  - Rationale: DRF defaults are admin-only in this project, which would prevent the endpoint from raising the intended exception during a simple browser check. The implementation should make verification straightforward while documenting that the endpoint intentionally fails.
  - Alternative considered: Leave default permissions in place. That would make the endpoint harder to verify and could capture authentication errors instead of the deliberate test exception.

## Risks / Trade-offs

- Intentionally failing endpoint could be called outside verification contexts -> Keep it clearly named, scoped to `sentry-debug`, and document that it exists for Sentry validation.
- DSN misconfiguration could silently prevent event delivery -> Add settings driven by `.env` and include a verification task that calls the debug endpoint and checks Sentry.
- Using 100% tracing/profiling sampling adds overhead -> This is acceptable for the requested basic verification setup, but production deployments may later lower sample rates.
- Enabling default PII sends request/user context to Sentry -> This follows the provided setup, but deployments should review privacy requirements before production use.
