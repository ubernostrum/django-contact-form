from django.conf import settings
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import RequestFactory
from django.test import TestCase

from ..forms import ContactForm


class ContactFormViewTests(TestCase):
    urls = 'contact_form.tests.test_urls'

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
