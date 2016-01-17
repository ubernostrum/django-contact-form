.. _quickstart:

Quick start guide
=================

First you'll need to have Django and ``django-contact-form``
installed; for details on that, see :ref:`the installation guide
<install>`.

Once that's done, you can start setting up
``django-contact-form``. Since it doesn't provide any database models
or use any other application-config mechanisms, you do *not* need to
add ``django-contact-form`` to your ``INSTALLED_APPS`` setting; you
can simply begin using it right away.


URL configuration
=================

The easiest way to set up the views in ``django-contact-form`` is to
just use the provided URLconf, found at ``contact_form.urls``. You can
include it wherever you like in your site's URL configuration; for
example, to have it live at the URL ``/contact/``:

.. code-block:: python

    from django.conf.urls import include, url


    urlpatterns = [
        # ... other URL patterns for your site ...
        url(r'^contact/', include('contact_form.urls')),
    ]

If you'll be using a custom form class, you'll need to manually set up
your URLs so you can tell ``django-contact-form`` about your form
class. For example:


.. code-block:: python

    from django.conf.urls import include, url
    from django.views.generic import TemplateView

    from contact_form.views import ContactFormView

    from yourapp.forms import YourCustomFormClass


    urlpatterns = [
        # ... other URL patterns for your site ...
        url(r'^contact/$',
            ContactFormView.as_view(
                form_class=YourCustomFormClass),
            name='contact_form'),
        url(r'^contact/sent/$',
            TemplateView.as_view(
                template_name='contact_form/contact_form_sent.html'),
            name='contact_form_sent'),
    ]


Required templates
==================

The two views above will need two templates to be created:

``contact_form/contact_form.html``
    This is used to display the contact form. It has a
    ``RequestContext`` (so any context processors will be applied),
    and also provides the form instance as the context variable
    ``form``.

``contact_form/contact_form_sent.html``
    This is used after a successful form submission, to let the user
    know their message has been sent. It has a ``RequestContext``, but
    provides no additional context variables of its own.

You'll also need to create at least two more templates to handle the
rendering of the message: ``contact_form/contact_form_subject.txt``
for the subject line of the email to send, and
``contact_form/contact_form.txt`` for the body (note that the file
extension for these is ``.txt``, not ``.html``!). Both of these will
receive a ``RequestContext`` with a set of variables named for the
fields of the form (by default: ``name``, ``email`` and ``body``), as
well as one more variable: ``site``, representing the current site
(either a ``Site`` or ``RequestSite`` instance, depending on whether
Django's sites framework is installed).

.. warning:: **Subject must be a single line**

   In order to prevent `header injection attacks
   <https://en.wikipedia.org/wiki/Email_injection>`_, the subject
   *must* be only a single line of text, and Django's email framework
   will reject any attempt to send an email with a multi-line
   subject. So it's a good idea to ensure your
   ``contact_form_subject.txt`` template only produces a single line
   of output when rendered; as a precaution, however,
   ``django-contact-form`` will split the output of this template at
   line breaks, then forcibly re-join it into a single line of text.
