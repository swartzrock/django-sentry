## Table of Contents
- [Installing Dependencies](#installing-dependencies)
- [Configuring Sentry](#configuring-sentry)
- [Running The Demo](#running-the-demo)
- [Cleaning Up](#cleaning-up)

## Installing Dependencies

This project requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

1. Install `uv`:
```
brew install uv
```

2. Install Sentry's command line tool for release tracking and commit integration:
```
npm install -g @sentry/cli
```

## Configuring Sentry

The Sentry client library requires a [DSN generated from Sentry](https://docs.sentry.io/quickstart/#configure-the-dsn). Update `myproject/settings.py`:

```python
sentry_sdk.init(
    dsn="https://yourdsn@sentry.io/1234567",
    integrations=[DjangoIntegration()],
)
```

Further details on configuring Sentry [here](https://docs.sentry.io/platforms/python/django/).

## Running The Demo

Install dependencies and start the server:
```
make deploy
```

This installs packages, creates a Sentry release, runs migrations, and starts the Django development server.

You can also run each step individually:
```
make install    # install Python dependencies via uv
make migrate    # run database migrations
make run_django # start the development server
```

### Demo Specs

This demo uses Django REST Framework and exposes 3 API endpoints:

1. `http://localhost:8000/handled` — generates a runtime error explicitly reported to Sentry via `capture_exception`
2. `http://localhost:8000/unhandled` — generates an unhandled runtime error
3. `http://localhost:8000/checkout` — used with the [Sentry React demo storefront](https://github.com/sentry-demos/react), or directly via the Django REST Framework web UI

To trigger an error via the `/checkout` endpoint, POST the following JSON:

```json
{
    "cart": [
        {"id": "wrench", "name": "Wrench", "price": 500},
        {"id": "wrench", "name": "Wrench", "price": 500}
    ],
    "email": "user@email.com"
}
```

![Alt Text](django_demo_setup.gif)

## Cleaning Up

Press Ctrl-C to stop the Django development server.

To remove the virtual environment created by uv:
```
rm -rf .venv
```
