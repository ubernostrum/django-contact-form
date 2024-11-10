.. _index:

django-contact-form |release|
=============================

``django-contact-form`` provides customizable contact-form functionality for
`Django <https://www.djangoproject.com/>`_-powered Web sites.

This application includes:

* An extensible base contact-form class which is also usable as-is for basic
  functionality (collecting a name, email address, and message)

* A subclass of the base form which uses the Akismet spam-filtering service to
  detect and reject spam submissions

* A class-based Django view which can be used with either of the built-in
  contact form classes, or your own customized form

For the default contact-form functionality, add ``"django_contact_form"`` to
your Django site's ``INSTALLED_APPS`` setting, add the following line to
your site's root URLConf, and create the templates specified in :ref:`the usage
guide <default-templates>`:

.. code-block:: python

    from django.urls import include, path


    urlpatterns = [
        # ... other URL patterns for your site ...
        path("contact/", include("django_contact_form.urls")),
    ]


.. toctree::
   :caption: Installation and usage
   :maxdepth: 1

   install
   usage

.. toctree::
   :caption: API reference
   :maxdepth: 1

   forms
   views

.. toctree::
   :caption: Other documentation
   :maxdepth: 1

   changelog
   faq
