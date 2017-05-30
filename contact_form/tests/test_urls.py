"""
URLConf for testing django-contact-form.

"""

from django.conf.urls import url
from django.views.generic import TemplateView

from ..forms import AkismetContactForm
from ..views import ContactFormView


urlpatterns = [
    url(r'^$',
        ContactFormView.as_view(),
        name='contact_form'),
    url(r'^sent/$',
        TemplateView.as_view(
            template_name='contact_form/contact_form_sent.html'
        ),
        name='contact_form_sent'),
    url(r'^test_recipient_list/$',
        ContactFormView.as_view(
            recipient_list=['recipient_list@example.com']),
        name='test_recipient_list'),
    url(r'^test_akismet_form/$',
        ContactFormView.as_view(
            form_class=AkismetContactForm
        ),
        name='test_akismet_form'),
]
