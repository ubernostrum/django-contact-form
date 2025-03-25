"""
Tests for the Akismet spam-filtering integration.

"""

# SPDX-License-Identifier: BSD-3-Clause

import os
from http import HTTPStatus
from unittest import mock

import akismet
from django.core.exceptions import ImproperlyConfigured
from django.test import RequestFactory, TestCase
from django.test.utils import override_settings
from django.urls import reverse

from django_contact_form._akismet import _clear_cached_instance, _try_get_akismet_client
from django_contact_form.forms import AkismetContactForm


class AlwaysSpamClient(akismet.TestSyncClient):
    """
    Akismet client which always marks content as spam.

    """

    comment_check_response = akismet.CheckResponse.SPAM


class NeverSpamClient(akismet.TestSyncClient):
    """
    Akismet client which always marks content as non-spam.

    """

    comment_check_response = akismet.CheckResponse.HAM


class ValidConfigClient(akismet.TestSyncClient):
    """
    Akismet client which marks its configuration as valid.

    """

    verify_key_response = True


class InvalidConfigClient(akismet.TestSyncClient):
    """
    Akismet client which marks its configuration as invalid.

    """

    verify_key_response = False


@override_settings(ROOT_URLCONF="django_contact_form.akismet_urls")
class AkismetContactFormTests(TestCase):
    """
    Tests for the Akismet contact form.

    """

    akismet_config = akismet.Config(key="test-key", url="http://example.com")

    payload = {
        "name": "Test Name",
        "email": "test@example.com",
        "body": "Test message.",
    }

    def setUp(self):
        """
        Ensure the Akismet client instance is not cached between tests.

        """
        _clear_cached_instance()

    def request(self):
        """
        Construct and return an HttpRequest object for test use.

        """
        return RequestFactory().request()

    def test_akismet_form_spam(self):
        """
        The Akismet contact form correctly rejects spam.

        """
        with (
            AlwaysSpamClient(config=self.akismet_config) as akismet_client,
            mock.patch(
                "django_contact_form._akismet._try_get_akismet_client",
                new=mock.Mock(return_value=akismet_client),
            ),
        ):
            form = AkismetContactForm(request=self.request(), data=self.payload)
            assert not form.is_valid()
            assert str(form.SPAM_MESSAGE) in form.errors["body"]

    def test_akismet_form_ham(self):
        """
        The Akismet contact form correctly accepts non-spam.

        """
        with (
            NeverSpamClient(config=self.akismet_config) as akismet_client,
            mock.patch(
                "django_contact_form._akismet._try_get_akismet_client",
                new=mock.Mock(return_value=akismet_client),
            ),
        ):
            form = AkismetContactForm(request=self.request(), data=self.payload)
            assert form.is_valid()

    def test_akismet_form_no_body(self):
        """
        The Akismet contact form correctly skips validation when no email body is
        provided.

        """
        data = {"name": "Test", "email": "email@example.com"}

        with (
            NeverSpamClient(config=self.akismet_config) as akismet_client,
            mock.patch(
                "django_contact_form._akismet._try_get_akismet_client",
                new=mock.Mock(return_value=akismet_client),
            ),
        ):
            form = AkismetContactForm(request=self.request(), data=data)
            assert not form.is_valid()

    def test_akismet_django_settings_invalid(self):
        """
        When the Django settings are present and invalid, ImproperlyConfigured is
        raised.

        """
        with (
            self.settings(
                AKISMET_API_KEY=self.akismet_config.key,
                AKISMET_BLOG_URL=self.akismet_config.url,
            ),
            self.assertRaises(ImproperlyConfigured),
        ):
            _try_get_akismet_client(InvalidConfigClient)

    def test_akismet_env_invalid(self):
        """
        When the environment variables are present and invalid, ImproperlyConfigured
        is raised.

        """
        try:
            os.environ["PYTHON_AKISMET_API_KEY"] = self.akismet_config.key
            os.environ["PYTHON_AKISMET_BLOG_URL"] = self.akismet_config.url
            with self.assertRaises(ImproperlyConfigured):
                _try_get_akismet_client(InvalidConfigClient)
        finally:
            del os.environ["PYTHON_AKISMET_API_KEY"]
            del os.environ["PYTHON_AKISMET_BLOG_URL"]

    def test_akismet_env_missing(self):
        """
        When the environment variables are missing, ImproperlyConfigured is raised.

        """
        for key in ("PYTHON_AKISMET_API_KEY", "PYTHON_AKISMET_BLOG_URL"):
            if key in os.environ:
                del os.environ[key]
        with self.assertRaises(ImproperlyConfigured):
            _try_get_akismet_client(InvalidConfigClient)

    def test_akismet_django_settings_valid(self):
        """
        When the Django settings are present and valid, an Akismet client is
        returned using them.

        """
        with self.settings(
            AKISMET_API_KEY=self.akismet_config.key,
            AKISMET_BLOG_URL=self.akismet_config.url,
        ):
            client = _try_get_akismet_client(ValidConfigClient)
            assert client is not None
            assert isinstance(client, ValidConfigClient)

    def test_akismet_env_valid(self):
        """
        When the environment variables are present and valid, an Akismet client is
        returned using them.

        """
        try:
            os.environ["PYTHON_AKISMET_API_KEY"] = self.akismet_config.key
            os.environ["PYTHON_AKISMET_BLOG_URL"] = self.akismet_config.url
            client = _try_get_akismet_client(ValidConfigClient)
            assert client is not None
            assert isinstance(client, ValidConfigClient)
        finally:
            del os.environ["PYTHON_AKISMET_API_KEY"]
            del os.environ["PYTHON_AKISMET_BLOG_URL"]

    def test_akismet_django_settings_persist(self):
        """
        A client created from Django settings is correctly persistsed and returned on
        later calls.

        """
        with self.settings(
            AKISMET_API_KEY=self.akismet_config.key,
            AKISMET_BLOG_URL=self.akismet_config.url,
        ):
            first = _try_get_akismet_client(ValidConfigClient)
            second = _try_get_akismet_client(ValidConfigClient)
            assert first is second

    def test_akismet_env_persist(self):
        """
        A client cretaed from environment variables is correctly persisted and returned
        on later calls.

        """
        try:
            os.environ["PYTHON_AKISMET_API_KEY"] = self.akismet_config.key
            os.environ["PYTHON_AKISMET_BLOG_URL"] = self.akismet_config.url
            first = _try_get_akismet_client(ValidConfigClient)
            second = _try_get_akismet_client(ValidConfigClient)
            assert first is second
        finally:
            del os.environ["PYTHON_AKISMET_API_KEY"]
            del os.environ["PYTHON_AKISMET_BLOG_URL"]

    @override_settings(ROOT_URLCONF="django_contact_form.akismet_urls")
    def test_akismet_view(self):
        """
        The Akismet contact form URL uses a spam-filtering AkismetContactForm
        instance.

        """
        response = self.client.get(reverse("django_contact_form"))
        assert response.status_code == HTTPStatus.OK
        assert isinstance(response.context["form"], AkismetContactForm)
