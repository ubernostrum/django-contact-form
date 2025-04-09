"""
Minimal Django settings file for test runs.

"""

# SPDX-License-Identifier: BSD-3-Clause

import pathlib

from django.utils.crypto import get_random_string

APP_DIR = pathlib.Path(__file__).parents[0]

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
DEFAULT_FROM_EMAIL = "noreply@example.com"
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django_contact_form",
    "tests",
)
MANAGERS = [("Manager", "noreply@example.com")]
MIDDLEWARE = (
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
)
ROOT_URLCONF = "django_contact_form.urls"
SECRET_KEY = get_random_string(12)
SITE_ID = 1
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [APP_DIR / "templates"],
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]
