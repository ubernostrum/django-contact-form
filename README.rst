.. -*-restructuredtext-*-

.. image:: https://github.com/ubernostrum/django-contact-form/workflows/CI/badge.svg
   :alt: CI status image
   :target: https://github.com/ubernostrum/django-contact-form/actions?query=workflow%3ACI

``django-contact-form`` provides customizable contact-form
functionality for `Django <https://www.djangoproject.com/>`_-powered
sites.

This application includes:

* An extensible base contact-form class which is also usable as-is for
  basic functionality (collecting a name, email address, and message)

* A subclass of the base form which uses the Akismet spam-filtering
  service to detect and reject spam submissions

* A class-based Django view which can be used with either of the
  built-in contact form classes, or your own customized form

For the default contact-form functionality, add
``"django_contact_form"`` to your Django site's ``INSTALLED_APPS``
setting, add the following line to your site's root URLConf, and
create the templates specified in `the usage guide
<https://django-contact-form.readthedocs.io/en/latest/usage.html#default-templates>`_:

.. code-block:: python

    from django.urls import include, path


    urlpatterns = [
        # ... other URL patterns for your site ...
        path("contact/", include("django_contact_form.urls")),
    ]

Full documentation for all functionality is `available online
<http://django-contact-form.readthedocs.io/>`_.
