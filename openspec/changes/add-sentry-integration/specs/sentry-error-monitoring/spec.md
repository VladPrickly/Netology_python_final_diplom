## ADDED Requirements

### Requirement: Sentry SDK initialization
The system SHALL initialize the Sentry Python SDK when Django settings are loaded using the configured project DSN.

#### Scenario: Django starts with Sentry configured
- **WHEN** the Django application imports its settings
- **THEN** the Sentry SDK is initialized with the configured DSN

### Requirement: Baseline Sentry options
The system SHALL configure Sentry with default PII capture enabled, log capture enabled, full tracing sampling, and full profiling sampling for the baseline integration.

#### Scenario: Sentry options are applied
- **WHEN** the Sentry SDK is initialized
- **THEN** `send_default_pii`, `enable_logs`, `traces_sample_rate`, `profile_session_sample_rate`, and `profile_lifecycle` are configured according to the provided setup

### Requirement: Sentry debug API endpoint
The system SHALL expose a DRF APIView endpoint at `/api/v1/sentry-debug` that raises an unhandled exception when requested.

#### Scenario: Developer triggers a test exception
- **WHEN** a developer sends a GET request to `/api/v1/sentry-debug`
- **THEN** the endpoint raises an unhandled exception that can be captured by Sentry

### Requirement: Dependency declaration
The system SHALL include `sentry-sdk` in the project Python dependencies so the integration is installed with the application.

#### Scenario: Dependencies are installed
- **WHEN** project dependencies are installed from `requirements.txt`
- **THEN** the Sentry Python SDK is installed for use by Django settings
