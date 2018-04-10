"""
A standalone test runner script, configuring the minimum settings
required for django-contact-form' tests to execute.

Re-use at your own risk: many Django applications will require full
settings and/or templates in order to execute their tests, while
django-contact-form does not.

"""

import os
import sys


# Make sure the app is (at least temporarily) on the import path.
APP_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, APP_DIR)


# Minimum settings required for django-contact-form to work.
SETTINGS_DICT = {
    'BASE_DIR': APP_DIR,
    'INSTALLED_APPS': [
        'contact_form',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sites',
    ],
    'ROOT_URLCONF': 'contact_form.tests.test_urls',
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(APP_DIR, 'db.sqlite3'),
        },
    },
    'MIDDLEWARE_CLASSES': (
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
    ),
    'SITE_ID': 1,
    'DEFAULT_FROM_EMAIL': 'contact@example.com',
    'MANAGERS': [('Manager', 'noreply@example.com')],
    'TEMPLATES': [{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(APP_DIR, 'tests/templates')],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    }],
}

try:
    from captcha.constants import TEST_PUBLIC_KEY, TEST_PRIVATE_KEY

    SETTINGS_DICT['INSTALLED_APPS'].append('captcha')
    SETTINGS_DICT.update({
        'RECAPTCHA_PUBLIC_KEY':  os.getenv('PYTHON_RECAPTCHA_PUBLIC_KEY',
                                           TEST_PUBLIC_KEY),
        'RECAPTCHA_PRIVATE_KEY': os.getenv('PYTHON_RECAPTCHA_PRIVATE_KEY',
                                           TEST_PRIVATE_KEY),
        'NOCAPTCHA': False,
        'RECAPTCHA_USE_SSL': True,
        'RECAPTCHA_LANG': 'en',
    })

except ImportError:
    captcha = None
    print("Importing captcha failed. "
          "Skipping all tests for ReCaptchaContactForm.")


def run_tests():
    # Making Django run this way is a two-step process. First, call
    # settings.configure() to give Django settings to work with:
    from django.conf import settings
    settings.configure(**SETTINGS_DICT)

    # Then, call django.setup() to initialize the application cache
    # and other bits:
    import django
    django.setup()

    # Now we instantiate a test runner...
    from django.test.utils import get_runner
    TestRunner = get_runner(settings)

    # And then we run tests and return the results.
    test_runner = TestRunner(verbosity=2, interactive=True)
    failures = test_runner.run_tests(['contact_form.tests'])
    sys.exit(bool(failures))


if __name__ == '__main__':
    run_tests()
