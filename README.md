# Trkr
A simple bug tracker


## Installation

Trkr uses [poetry](https://python-poetry.org/docs/#installation) for dependency management
```shell script
poetry install --no-dev
```

For running Trkr in production, pick a Django secret key, and set it to an environemt variable called `DJANGO_SECRET_KEY`.
For local development, `SECRET_KEY` is set in `trkr.settings.dev`. 


## Local development
Install all dependencies using [poetry](https://python-poetry.org/docs/#installation).
```shell script
poetry install
```

Run migrations and create a superuser. By default, a sqlite3 database will be used. 
```shell script
python manage.py migrate
python manage.py createsuperuser
```
Run the project locally.
```shell script
DJANGO_SETTINGS_MODULE=trkr.settings.dev python3 manage.py runserver 8000
```

Trkr comes with a set of linters and formatters in dev requirements, please use them before committing any changes.
```shell script
black .
isort .
pylint *.py
```

## Planned features
* issues model
  * title
  * description
  * category
  * reporter
  * assignee
  * status
  * estimated time
  * spent time
* category model
  * editable
  * comes with defaults
* test coverage
* user roles
  * superuser
  * staff (read-only)
* REST API
