# Login History Too

![Coverage](https://img.shields.io/badge/coverage-74%25-brightgreen)

## Overview

Simple login history tracking including IP address (along with its geo data), User Agent data and timestamp.

## Quickstart

Install Login History Too:

```bash
pip install login-history-too
```

### Settings

To enable `login_history_too` in your project you need to add it to `INSTALLED_APPS` in your projects `settings.py` file:

```python
INSTALLED_APPS = (
    ...
    'login_history_too',
    ...
)
```

If you want to override the `GEOLOCATION_METHOD` to use another geolocation API:

```python
LOGIN_HISTORY_TOO = {
    "GEOLOCATION_METHOD": "login_history_too.utils.get_ip_info"
}
```

## Development

```bash
make env
make pip_install
make migrations
make migrate
make superuser
make serve
```

- Visit `http://127.0.0.1:8000/` for the default "It worked" page
- Visit `http://127.0.0.1:8000/admin/` for the Django Admin

### Testing

```bash
make pytest
make coverage
make open_coverage
```

## Deploying

```bash
# Publish to PyPI Test before the live PyPi
make release_test
make release
```

## Issues

If you experience any issues, please create an [issue](https://github.org/tsantor/login-history-too/issues) on Github.
