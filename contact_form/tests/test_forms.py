import os
import unittest

import mock

from django.conf import settings
from django.core import mail
from django.test import RequestFactory, TestCase
from django.utils.six import text_type

from ..forms import AkismetContactForm, ReCaptchaContactForm, ContactForm


class ContactFormTests(TestCase):
    """
    Tests the base ContactForm.

    """
    valid_data = {'name': 'Test',
                  'email': 'test@example.com',
                  'body': 'Test message'}

    def request(self):
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
        data = {'name': 'Test',
                'body': 'Test message'}
        form = ContactForm(request=self.request(), data=data)
        self.assertRaises(ValueError, form.get_message_dict)
        self.assertRaises(ValueError, form.get_context)

    def test_send(self):
        """
        Valid form can and does in fact send email.

        """
        form = ContactForm(request=self.request(),
                           data=self.valid_data)
        self.assertTrue(form.is_valid())

        form.save()
        self.assertEqual(1, len(mail.outbox))

        message = mail.outbox[0]
        self.assertTrue(self.valid_data['body'] in message.body)
        self.assertEqual(settings.DEFAULT_FROM_EMAIL,
                         message.from_email)
        self.assertEqual(form.recipient_list,
                         message.recipients())

    def test_no_sites(self):
        """
        Sites integration works with or without installed
        contrib.sites.

        """
        with self.modify_settings(
            INSTALLED_APPS={
                'remove': ['django.contrib.sites'],
                }):
            form = ContactForm(request=self.request(),
                               data=self.valid_data)
            self.assertTrue(form.is_valid())

            form.save()
            self.assertEqual(1, len(mail.outbox))

    def test_recipient_list(self):
        """
        Passing recipient_list when instantiating ContactForm properly
        overrides the list of recipients.

        """
        recipient_list = ['recipient_list@example.com']
        form = ContactForm(request=self.request(),
                           data=self.valid_data,
                           recipient_list=recipient_list)
        self.assertTrue(form.is_valid())

        form.save()
        self.assertEqual(1, len(mail.outbox))

        message = mail.outbox[0]
        self.assertEqual(recipient_list,
                         message.recipients())

    def test_callable_template_name(self):
        """
        When a template_name() method is defined, it is used and
        preferred over a 'template_name' attribute.

        """
        class CallableTemplateName(ContactForm):
            def template_name(self):
                return 'contact_form/test_callable_template_name.html'

        form = CallableTemplateName(request=self.request(),
                                    data=self.valid_data)
        self.assertTrue(form.is_valid())

        form.save()
        self.assertEqual(1, len(mail.outbox))

        message = mail.outbox[0]
        self.assertTrue('Callable template_name used.' in
                        message.body)

    def test_callable_message_parts(self):
        """
        Message parts implemented as methods are called and preferred
        over attributes.

        """
        overridden_data = {
            'from_email': 'override@example.com',
            'message': 'Overridden message.',
            'recipient_list': ['override_recpt@example.com'],
            'subject': 'Overridden subject',
        }

        class CallableMessageParts(ContactForm):
            def from_email(self):
                return overridden_data['from_email']

            def message(self):
                return overridden_data['message']

            def recipient_list(self):
                return overridden_data['recipient_list']

            def subject(self):
                return overridden_data['subject']

        form = CallableMessageParts(request=self.request(),
                                    data=self.valid_data)
        self.assertTrue(form.is_valid())

        self.assertEqual(overridden_data,
                         form.get_message_dict())


@unittest.skipUnless(
    getattr(
        settings,
        'AKISMET_API_KEY',
        os.getenv('PYTHON_AKISMET_API_KEY')
    ) is not None,
    "AkismetContactForm requires Akismet configuration"
)
class AkismetContactFormTests(TestCase):
    """
    Tests the Akismet contact form.

    """
    def request(self):
        return RequestFactory().request()

    def test_akismet_form_spam(self):
        """
        The Akismet contact form correctly rejects spam.

        """
        data = {'name': 'viagra-test-123',
                'email': 'email@example.com',
                'body': 'This is spam.'}
        with mock.patch('akismet.Akismet', autospec=True) as akismet_mock:
            instance = akismet_mock.return_value
            instance.verify_key.return_value = True
            instance.comment_check.return_value = True
            form = AkismetContactForm(
                request=self.request(),
                data=data
            )
            self.assertFalse(form.is_valid())
            self.assertTrue(
                text_type(form.SPAM_MESSAGE) in
                form.errors['body']
            )

    def test_akismet_form_ham(self):
        """
        The Akismet contact form correctly accepts non-spam.

        """
        data = {'name': 'Test',
                'email': 'email@example.com',
                'body': 'Test message.'}
        with mock.patch('akismet.Akismet', autospec=True) as akismet_mock:
            instance = akismet_mock.return_value
            instance.verify_key.return_value = True
            instance.comment_check.return_value = False
            form = AkismetContactForm(
                request=self.request(),
                data=data
            )
            self.assertTrue(form.is_valid())


class ReCaptchaContactFormTests(TestCase):
    """
    Tests the ReCaptcha contact form.

    """
    valid_data = {'name': 'Test',
                  'email': 'test@example.com',
                  'body': 'Test message'}

    def setUp(self):
        os.environ['RECAPTCHA_TESTING'] = 'True'

    def request(self):
        return RequestFactory().request()

    def test_captcha_envvar_enabled(self):
        data = self.valid_data
        data.update({'g-recaptcha-response': 'PASSED'}
                    if getattr(settings, 'NOCAPTCHA', True) else
                    {'recaptcha_response_field': 'PASSED'})
        form = ReCaptchaContactForm(
            request=self.request(),
            data=data
        )
        self.assertTrue(form.is_valid())

    def test_captcha_envvar_disabled(self):
        os.environ['RECAPTCHA_TESTING'] = 'False'
        data = self.valid_data
        data.update({'g-recaptcha-response': 'PASSED'}
                    if getattr(settings, 'NOCAPTCHA', True) else
                    {'recaptcha_response_field': 'PASSED'})
        form = ReCaptchaContactForm(
            request=self.request(),
            data=data
        )
        self.assertFalse(form.is_valid())

    def tearDown(self):
        del os.environ['RECAPTCHA_TESTING']
        pass
