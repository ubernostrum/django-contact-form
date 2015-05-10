from django.conf import settings
from django.core import mail
from django.test import RequestFactory
from django.test import TestCase

from django.contrib.sites.models import Site

from ..forms import ContactForm


class ContactFormTests(TestCase):
    def test_request_required(self):
        """
        Can't instantiate without an HttpRequest.
        
        """
        self.assertRaises(TypeError, ContactForm)

    def test_valid_data_required(self):
        """
        Can't try to build the message dict unless data is valid.
        
        """
        request = RequestFactory().request()
        data = {'name': 'Test',
                'body': 'Test message'}
        form = ContactForm(request=request, data=data)
        self.assertRaises(ValueError, form.get_message_dict)

    def test_send(self):
        """
        Valid form can and does in fact send email.
        
        """
        request = RequestFactory().request()
        data = {'name': 'Test',
                'email': 'test@example.com',
                'body': 'Test message'}
        form = ContactForm(request=request, data=data)
        self.assertTrue(form.is_valid())

        form.save()
        self.assertEqual(1, len(mail.outbox))

        message = mail.outbox[0]
        self.assertTrue(data['body'] in message.body)
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
            request = RequestFactory().request()
            data = {'name': 'Test',
                    'email': 'test@example.com',
                    'body': 'Test message'}
            form = ContactForm(request=request, data=data)
            self.assertTrue(form.is_valid())

            form.save()
            self.assertEqual(1, len(mail.outbox))

    def test_recipient_list(self):
        """
        Passing recipient_list when instantiating ContactForm properly
        overrides the list of recipients.

        """
        recipient_list = ['recipient_list@example.com']
        request = RequestFactory().request()
        data = {'name': 'Test',
                'email': 'test@example.com',
                'body': 'Test message'}
        form = ContactForm(request=request, data=data,
                           recipient_list=recipient_list)
        self.assertTrue(form.is_valid())

        form.save()
        self.assertEqual(1, len(mail.outbox))

        message = mail.outbox[0]
        self.assertEqual(recipient_list,
                         message.recipients())
