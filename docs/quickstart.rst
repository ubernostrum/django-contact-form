.. _quickstart:

Quick start guide
=================

First you'll need to have Django and django-contact-form
installed; for details on that, see :ref:`the installation guide
<install>`.

Once that's done, you can start setting up
django-contact-form. Since it doesn't provide any database models
or use any other application-config mechanisms, you do *not* need to
add django-contact-form to your ``INSTALLED_APPS`` setting; you
can begin using it right away.


URL configuration
-----------------

The quicket way to set up the views in django-contact-form is to use
the provided URLconf, found at ``contact_form.urls``. You can include
it wherever you like in your site's URL configuration; for example, to
have it live at the URL ``/contact/``:

.. code-block:: python

    from django.conf.urls import include, url


    urlpatterns = [
        # ... other URL patterns for your site ...
        url(r'^contact/', include('contact_form.urls')),
    ]

If you'll be using a custom form class, you'll need to manually set up
your URLs so you can tell django-contact-form about your form
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
                form_class=YourCustomFormClass
            ),
            name='contact_form'),
        url(r'^contact/sent/$',
            TemplateView.as_view(
                template_name='contact_form/contact_form_sent.html'
            ),
            name='contact_form_sent'),
    ]

.. important:: **Where to put custom forms and views**

   When writing a custom form class (or custom ``ContactFormView``
   subclass), **don't** put your custom code inside
   django-contact-form. Instead, put your custom code in the
   appropriate place (a ``forms.py`` or ``views.py`` file) in an
   application you've written.


Required templates
------------------

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
`Django's sites framework
<https://docs.djangoproject.com/en/1.11/ref/contrib/sites/>`_ is
installed).

.. warning:: **Subject must be a single line**

   In order to prevent `header injection attacks
   <https://en.wikipedia.org/wiki/Email_injection>`_, the subject
   *must* be only a single line of text, and Django's email framework
   will reject any attempt to send an email with a multi-line
   subject. So it's a good idea to ensure your
   ``contact_form_subject.txt`` template only produces a single line
   of output when rendered; as a precaution, however,
   django-contact-form will split the output of this template at
   line breaks, then forcibly re-join it into a single line of text.


Using a spam-filtering contact form
-----------------------------------

Spam filtering is a common desire for contact forms, due to the large
amount of spam they can attract. There is a spam-filtering contact
form class included in django-contact-form:
:class:`~contact_forms.forms.AkismetContactForm`, which uses `the
Wordpress Akismet spam-detection service <https://akismet.com/>`_.

To use this form, you will need to do the following things:

1. Install the Python ``akismet`` module to allow django-contact-form
   to communicate with the Akismet service. You can do this via ``pip
   install akismet``, or as you install django-contact-form via ``pip
   install django-contact-form[akismet]``.

2. Obtain an Akismet API key from <https://akismet.com/>, and
   associate it with the URL of your site.

3. Supply the API key and URL for django-contact-form to use. You can
   either place them in the Django settings ``AKISMET_API_KEY`` and
   ``AKISMET_BLOG_URL``, or in the environment variables
   ``PYTHON_AKISMET_API_KEY`` and ``PYTHON_AKISMET_BLOG_URL``.

Then you can replace the suggested URLconf above with the following:

.. code-block:: python

    from django.conf.urls import include, url


    urlpatterns = [
        # ... other URL patterns for your site ...
        url(r'^contact/', include('contact_form.akismet_urls')),
    ]

