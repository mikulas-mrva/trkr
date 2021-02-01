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
export DJANGO_SETTINGS_MODULE=trkr.settings.dev
python manage.py migrate
python manage.py loaddata categories
python manage.py createsuperuser --username admin --email admin@example.com
```
Run the project locally.
```shell script
python manage.py runserver 8000
```

Trkr comes with a set of linters and formatters in dev requirements, please use them before committing any changes.
```shell script
black .
isort .
pylint *.py
```
