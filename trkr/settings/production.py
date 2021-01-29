import os

from trkr.settings.base import *  # noqa

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
