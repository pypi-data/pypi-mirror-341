# Dfhir(Django FHIR) API

API backend for carefusion365

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands


To simply run the backend without using docker, you may need to set the following env variables:

```
# type these in your terminal

export DATABASE_URL=postgres://postgres:postgres@localhost:5432/nebula # assumes a database called nebula is created with username postgres and password postgres
export CELERY_BROKER_URL='redis://127.0.0.1:6379/0' # uses a redis broker. You need redis installed if not you can use memcache url
export USE_DOCKER = "no"

```
Alternatively you can run these commands inline while starting the server:

```
DATABASE_URL=postgres://postgres:postgres@localhost:5432/nebula CELERY_BROKER_URL='redis://127.0.0.1:6379/0'  USE_DOCKER="no" python manage.py runserver
```

### Running migrations

To run the app, you need to run migrations of all tables created. To do do, run the command below:

```shell
python manage.py migrate
```

### Loading fixtures
Some tables like PractitionerRoleCode, ServiceCategory, etc come with preloaded fixtures. It is important
you load fixtures before running the app. To run fixtures, run the command below:

```shell
>> python manage.py loaddata practitioner_role_code.json
>> python manage.py loaddata service_category_valuesets.json
>> python manage.py loaddata clinical_specialty_valuesets.json
>> python manage.py loaddata service_type_valuesets.json
```

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy nebula

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

### Celery

This app comes with Celery.

To run a celery worker:

```bash
cd nebula
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important _where_ the celery commands are run. If you are in the same folder with _manage.py_, you should be right.

To run [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), you'll need to start the celery beat scheduler service. You can start it as a standalone process:

```bash
cd nebula
celery -A config.celery_app beat
```

or you can embed the beat service inside a worker with the `-B` option (not recommended for production use):

```bash
cd nebula
celery -A config.celery_app worker -B -l info
```

### Sentry

Sentry is an error logging aggregator service. You can sign up for a free account at <https://sentry.io/signup/?code=cookiecutter> or download and host it yourself.
The system is set up with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).
