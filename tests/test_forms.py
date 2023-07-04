"""
Tests for the built-in form classes.

"""

import os
import unittest
from unittest import mock

from django.conf import settings
from django.core import mail
from django.test import RequestFactory, TestCase

from django_contact_form.forms import AkismetContactForm, ContactForm


class ContactFormTests(TestCase):
    """
    Tests the base ContactForm.

    """

    valid_data = {"name": "Test", "email": "test@example.com", "body": "Test message"}

    def request(self):
        """
        Construct and return an HttpRequest object for test use.

        """
        return RequestFactory().request()

    def test_request_required(self):
        """
        Can't instantiate without an HttpRequest.

        """
        self.assertRaises(TypeError, ContactForm)

    def test_valid_data_required(self):
        """
        Can't try to build the message dict unless data is valid.

        """
        data = {"name": "Test", "body": "Test message"}
        form = ContactForm(request=self.request(), data=data)
        self.assertRaises(ValueError, form.get_message_dict)
        self.assertRaises(ValueError, form.get_message_context)

    def test_send(self):
        """
        Valid form can and does in fact send email.

        """
        form = ContactForm(request=self.request(), data=self.valid_data)
        self.assertTrue(form.is_valid())

        form.save()
        self.assertEqual(1, len(mail.outbox))

        message = mail.outbox[0]
        self.assertTrue(self.valid_data["body"] in message.body)
        self.assertEqual(settings.DEFAULT_FROM_EMAIL, message.from_email)
        self.assertEqual(form.recipient_list, message.recipients())

    def test_no_sites(self):
        """
        Sites integration works with or without installed
        contrib.sites.

        """
        with self.modify_settings(INSTALLED_APPS={"remove": ["django.contrib.sites"]}):
            form = ContactForm(request=self.request(), data=self.valid_data)
            self.assertTrue(form.is_valid())

            form.save()
            self.assertEqual(1, len(mail.outbox))

    def test_recipient_list(self):
        """
        Passing recipient_list when instantiating ContactForm properly
        overrides the list of recipients.

        """
        recipient_list = ["recipient_list@example.com"]
        form = ContactForm(
            request=self.request(), data=self.valid_data, recipient_list=recipient_list
        )
        self.assertTrue(form.is_valid())

        form.save()
        self.assertEqual(1, len(mail.outbox))

        message = mail.outbox[0]
        self.assertEqual(recipient_list, message.recipients())

    def test_callable_template_name(self):
        """
        When a template_name() method is defined, it is used and
        preferred over a 'template_name' attribute.

        """

        class CallableTemplateName(ContactForm):
            """
            Form with a template_name() method instead of a template_name attribute.

            """

            # pylint: disable=invalid-overridden-method
            def template_name(self):
                """
                Return the template name as a method rather than an attribute.

                """
                return "django_contact_form/test_callable_template_name.html"

        form = CallableTemplateName(request=self.request(), data=self.valid_data)
        self.assertTrue(form.is_valid())

        form.save()
        self.assertEqual(1, len(mail.outbox))

        message = mail.outbox[0]
        self.assertTrue("Callable template_name used." in message.body)

    def test_callable_message_parts(self):
        """
        Message parts implemented as methods are called and preferred
        over attributes.

        """
        overridden_data = {
            "from_email": "override@example.com",
            "message": "Overridden message.",
            "recipient_list": ["override_recpt@example.com"],
            "subject": "Overridden subject",
        }

        class CallableMessageParts(ContactForm):
            """
            Form with the message parts as methods rather than attributes.

            """

            def from_email(self):
                """
                Method returning the from_email.

                """
                return overridden_data["from_email"]

            def message(self):
                """
                Method returning the message.

                """
                return overridden_data["message"]

            def recipient_list(self):  # pylint: disable=method-hidden
                """
                Method returning the recipient_list.

                """
                return overridden_data["recipient_list"]

            def subject(self):
                """
                Method returning the subject.

                """
                return overridden_data["subject"]

        form = CallableMessageParts(request=self.request(), data=self.valid_data)
        self.assertTrue(form.is_valid())

        self.assertEqual(overridden_data, form.get_message_dict())


@unittest.skipUnless(
    getattr(settings, "AKISMET_API_KEY", os.getenv("PYTHON_AKISMET_API_KEY"))
    is not None,
    "AkismetContactForm requires Akismet configuration",
)
class AkismetContactFormTests(TestCase):
    """
    Tests the Akismet contact form.

    """

    def request(self):
        """
        Construct and return an HttpRequest object for test use.

        """
        return RequestFactory().request()

    def test_akismet_form_spam(self):
        """
        The Akismet contact form correctly rejects spam.

        """
        data = {
            "name": "viagra-test-123",
            "email": "email@example.com",
            "body": "This is spam.",
        }
        with mock.patch("akismet.Akismet", autospec=True) as akismet_mock:
            instance = akismet_mock.return_value
            instance.verify_key.return_value = True
            instance.comment_check.return_value = True
            form = AkismetContactForm(request=self.request(), data=data)
            self.assertFalse(form.is_valid())
            self.assertTrue(str(form.SPAM_MESSAGE) in form.errors["body"])

    def test_akismet_form_ham(self):
        """
        The Akismet contact form correctly accepts non-spam.

        """
        data = {"name": "Test", "email": "email@example.com", "body": "Test message."}
        with mock.patch("akismet.Akismet", autospec=True) as akismet_mock:
            instance = akismet_mock.return_value
            instance.verify_key.return_value = True
            instance.comment_check.return_value = False
            form = AkismetContactForm(request=self.request(), data=data)
            self.assertTrue(form.is_valid())

    def test_akismet_form_no_body(self):
        """
        The Akismet contact form correctly skips validation when no email
        body is provided.

        """
        data = {"name": "Test", "email": "email@example.com"}
        with mock.patch("akismet.Akismet", autospec=True) as akismet_mock:
            form = AkismetContactForm(request=self.request(), data=data)
            self.assertFalse(form.is_valid())
            akismet_mock.assert_not_called()
            self.assertFalse(form.is_valid())
