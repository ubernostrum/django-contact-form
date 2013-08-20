django-contact-form |version|
=============================

Providing some sort of contact or feedback form for soliciting
information from site visitors is a common need in web development,
and writing a contact form and associated handler view, while
relatively straightforward to do with `Django
<https://www.djangoproject.com/>`_, can be a tedious and repetitive
task.

This application aims to remove or reduce that tedium and repetition
by providing simple, extensible contact-form functionality for
Django-powered sites.

In the simplest case, all that's required is a bit of configuration
and a few templates, and one pattern in your URLConf:

.. code-block:: python

    (r'^contact/', include('contact_form.urls')),


Contents:

.. toctree::
   :maxdepth: 1

   quickstart
   forms
   views
   faq