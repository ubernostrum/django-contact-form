from django.conf import settings
from django.core import mail
from django.test import RequestFactory
from django.test import TestCase

from ..forms import ContactForm


class ContactFormTests(TestCase):
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
