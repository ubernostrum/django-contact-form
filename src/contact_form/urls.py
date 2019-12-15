"""
Example URLConf for a contact form.

If all you want is the basic ContactForm with default behavior,
include this URLConf somewhere in your URL hierarchy (for example, at
``/contact/``)

"""

from django.urls import path
from django.views.generic import TemplateView

from contact_form.views import ContactFormView


urlpatterns = [
    path("", ContactFormView.as_view(), name="contact_form"),
    path(
        "sent/",
        TemplateView.as_view(template_name="contact_form/contact_form_sent.html"),
        name="contact_form_sent",
    ),
]
