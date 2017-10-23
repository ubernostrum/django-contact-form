django-contact-form |release|
=============================

django-contact-form provides customizable contact-form functionality
for `Django <https://www.djangoproject.com/>`_-powered Web sites.

Basic functionality (collecting a name, email address and message) can
be achieved out of the box by setting up a few templates and adding
one line to your site's root URLconf:

.. code-block:: python

    url(r'^contact/', include('contact_form.urls')),

For notes on getting started quickly, and on how to customize
django-contact-form's behavior, read through the full documentation
below.


Contents:

.. toctree::
   :caption: Installation and configuration
   :maxdepth: 1

   install
   quickstart

.. toctree::
   :caption: For developers
   :maxdepth: 1

   forms
   views

.. toctree::
   :caption: Other documentation
   :maxdepth: 1

   faq