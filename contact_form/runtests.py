"""
A standalone test runner script, configuring the minimum settings
required for django-contact-form' tests to execute.

Re-use at your own risk: many Django applications will require full
settings and/or templates in order to execute their tests, while
django-contact-form does not.

"""

import os
import sys


# Make sure django-contact-form is (at least temporarily) on the
# import path.
CONTACT_FORM_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, CONTACT_FORM_DIR)


# Minimum settings required for django-contact-form to work.
SETTINGS_DICT = {
    'BASE_DIR': CONTACT_FORM_DIR,
    'INSTALLED_APPS': ('contact_form', 'django.contrib.sites'),
    'ROOT_URLCONF': 'contact_form.tests.urls',
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(CONTACT_FORM_DIR, 'db.sqlite3'),
        },
    },
    'MIDDLEWARE_CLASSES': (
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
    ),
    'TEMPLATE_DIRS': (
        os.path.join(CONTACT_FORM_DIR, 'tests/templates'),
    ),
    'SITE_ID': 1,
    'DEFAULT_FROM_EMAIL': 'contact@example.com',
    'MANAGERS': [('Manager', 'noreply@example.com')],
}


def run_tests():
    # Making Django run this way is a two-step process. First, call
    # settings.configure() to give Django settings to work with:
    from django.conf import settings
    settings.configure(**SETTINGS_DICT)

    # Then, call django.setup() to initialize the application cache
    # and other bits:
    import django
    if hasattr(django, 'setup'):
        django.setup()

    # Now we instantiate a test runner...
    from django.test.utils import get_runner
    TestRunner = get_runner(settings)

    # And then we run tests and return the results.
    test_runner = TestRunner(verbosity=1, interactive=True)
    failures = test_runner.run_tests(['contact_form.tests'])
    sys.exit(bool(failures))
