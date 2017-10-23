import os
import unittest

from django.conf import settings
from django.core import mail
from django.test import RequestFactory, TestCase
from django.test.utils import override_settings

from ..forms import ContactForm

try:
    from django.urls import reverse
except ImportError:  # pragma: no cover
    from django.core.urlresolvers import reverse  # pragma: no cover


@override_settings(ROOT_URLCONF='contact_form.tests.test_urls')
class ContactFormViewTests(TestCase):

    def test_get(self):
        """
        HTTP GET on the form view just shows the form.

        """
        contact_url = reverse('contact_form')

        response = self.client.get(contact_url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response,
                                'contact_form/contact_form.html')

    def test_send(self):
        """
        Valid data through the view results in a successful send.

        """
        contact_url = reverse('contact_form')
        data = {'name': 'Test',
                'email': 'test@example.com',
                'body': 'Test message'}

        response = self.client.post(contact_url,
                                    data=data)

        self.assertRedirects(response,
                             reverse('contact_form_sent'))

        self.assertEqual(1, len(mail.outbox))

        message = mail.outbox[0]
        self.assertTrue(data['body'] in message.body)
        self.assertEqual(settings.DEFAULT_FROM_EMAIL,
                         message.from_email)
        form = ContactForm(request=RequestFactory().request)
        self.assertEqual(form.recipient_list,
                         message.recipients())

    def test_invalid(self):
        """
        Invalid data doesn't work.

        """
        contact_url = reverse('contact_form')
        data = {'name': 'Test',
                'body': 'Test message'}

        response = self.client.post(contact_url,
                                    data=data)

        self.assertEqual(200, response.status_code)
        self.assertFormError(response,
                             'form',
                             'email',
                             'This field is required.')
        self.assertEqual(0, len(mail.outbox))

    def test_recipient_list(self):
        """
        Passing recipient_list when instantiating ContactFormView
        properly overrides the list of recipients.

        """
        contact_url = reverse('test_recipient_list')
        data = {'name': 'Test',
                'email': 'test@example.com',
                'body': 'Test message'}

        response = self.client.post(contact_url,
                                    data=data)
        self.assertRedirects(response,
                             reverse('contact_form_sent'))
        self.assertEqual(1, len(mail.outbox))

        message = mail.outbox[0]
        self.assertEqual(['recipient_list@example.com'],
                         message.recipients())


@unittest.skipUnless(
    getattr(
        settings,
        'AKISMET_API_KEY',
        os.getenv('PYTHON_AKISMET_API_KEY')
    ) is not None,
    "AkismetContactForm requires Akismet configuration"
)
class AkismetContactFormViewTests(TestCase):
    """
    Tests the views with the Akismet contact form.

    """
    def test_akismet_view_spam(self):
        """
        The Akismet contact form errors on spam.

        """
        contact_url = reverse('test_akismet_form')
        data = {'name': 'viagra-test-123',
                'email': 'email@example.com',
                'body': 'This is spam.'}
        response = self.client.post(contact_url,
                                    data=data)
        self.assertEqual(200, response.status_code)
        self.assertFalse(response.context['form'].is_valid())
        self.assertTrue(response.context['form'].has_error('body'))

    def test_akismet_view_ham(self):
        contact_url = reverse('test_akismet_form')
        data = {'name': 'Test',
                'email': 'email@example.com',
                'body': 'Test message.'}
        response = self.client.post(contact_url,
                                    data=data)
        self.assertRedirects(response,
                             reverse('contact_form_sent'))
        self.assertEqual(1, len(mail.outbox))

        message = mail.outbox[0]
        self.assertEqual(['noreply@example.com'],
                         message.recipients())
