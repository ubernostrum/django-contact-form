"""
Tests for the built-in views.

"""

# SPDX-License-Identifier: BSD-3-Clause

from http import HTTPStatus

import django
from django.conf import settings
from django.core import mail
from django.test import RequestFactory, TestCase
from django.test.utils import override_settings
from django.urls import reverse

from django_contact_form.forms import AkismetContactForm, ContactForm


@override_settings(ROOT_URLCONF="tests.test_urls")
class ContactFormViewTests(TestCase):
    """
    Tests for the built-in ContactFormView.

    """

    def test_get(self):
        """
        HTTP GET on the form view just shows the form.

        """
        contact_url = reverse("django_contact_form")

        response = self.client.get(contact_url)
        assert HTTPStatus.OK == response.status_code
        self.assertTemplateUsed(response, "django_contact_form/contact_form.html")

    def test_send(self):
        """
        Valid data through the view results in a successful send.

        """
        contact_url = reverse("django_contact_form")
        data = {"name": "Test", "email": "test@example.com", "body": "Test message"}

        response = self.client.post(contact_url, data=data)

        self.assertRedirects(response, reverse("django_contact_form_sent"))

        assert 1 == len(mail.outbox)

        message = mail.outbox[0]
        assert data["body"] in message.body
        assert settings.DEFAULT_FROM_EMAIL == message.from_email

        form = ContactForm(request=RequestFactory().request)
        assert form.recipient_list == message.recipients()

    def test_invalid(self):
        """
        Invalid data doesn't work.

        """
        contact_url = reverse("django_contact_form")
        data = {"name": "Test", "body": "Test message"}

        response = self.client.post(contact_url, data=data)

        assert HTTPStatus.OK == response.status_code
        # The argument signature of assertFormError() changed beginning in Django 4.1 --
        # prior to that the first argument was a response object, and after the
        # deprecation cycle completed in 5.0 the first argument is now the form
        # instance.
        if django.get_version() < "4.2":
            self.assertFormError(response, "form", "email", "This field is required.")
        else:
            self.assertFormError(
                response.context["form"], "email", "This field is required."
            )
        self.assertEqual(0, len(mail.outbox))

    def test_recipient_list(self):
        """
        Passing recipient_list when instantiating ContactFormView
        properly overrides the list of recipients.

        """
        contact_url = reverse("test_recipient_list")
        data = {"name": "Test", "email": "test@example.com", "body": "Test message"}

        response = self.client.post(contact_url, data=data)
        self.assertRedirects(response, reverse("django_contact_form_sent"))
        assert 1 == len(mail.outbox)

        message = mail.outbox[0]
        assert ["recipient_list@example.com"] == message.recipients()

    @override_settings(ROOT_URLCONF="django_contact_form.akismet_urls")
    def test_akismet_view(self):
        """
        The Akismet contact form URL uses a spam-filtering AkismetContactForm
        instance.

        """
        response = self.client.get(reverse("django_contact_form"))
        assert response.status_code == HTTPStatus.OK
        assert isinstance(response.context["form"], AkismetContactForm)
