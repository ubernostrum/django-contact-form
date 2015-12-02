.. _install:


Installation guide
==================

Before installing ``django-contact-form``, you'll need to have a copy
of `Django <https://www.djangoproject.com>`_ already installed. For
information on obtaining and installing Django, consult the `Django
download page <https://www.djangoproject.com/download/>`_, which
offers convenient packaged downloads and installation instructions.

The |version| release of ``django-contact-form`` supports Django 1.7
and 1.8, on any of Python 2.7, 3.3, 3.4, or 3.5. Older versions of Django
and/or Python may work, but are not tested or officially supported.


Normal installation
-------------------

The preferred method of installing ``django-contact-form`` is via
``pip``, the standard Python package-installation tool. If you don't
have ``pip``, instructions are available for `how to obtain and
install it <https://pip.pypa.io/en/latest/installing.html>`_.

Once you have ``pip``, simply type::

    pip install django-contact-form


Manual installation
-------------------

It's also possible to install ``django-contact-form`` manually. To do
so, obtain the latest packaged version from `the listing on the Python
Package Index
<https://pypi.python.org/pypi/django-contact-form/>`_. Unpack the
``.tar.gz`` file, and run::

    python setup.py install

Once you've installed ``django-contact-form``, you can verify
successful installation by opening a Python interpreter and typing
``import contact_form``.

If the installation was successful, you'll simply get a fresh Python
prompt. If you instead see an ``ImportError``, check the configuration
of your install tools and your Python import path to ensure
``django-contact-form`` installed into a location Python can import
from.


Installing from a source checkout
---------------------------------

The development repository for ``django-contact-form`` is at
<https://github.com/ubernostrum/django-contact-form>. Presuming you
have `git <http://git-scm.com/>`_ installed, you can obtain a copy of
the repository by typing::

    git clone https://github.com/ubernostrum/django-contact-form.git

From there, you can use normal git commands to check out the specific
revision you want, and install it using ``python setup.py install``.


Basic configuration and use
---------------------------

Once installed, only a small amount of setup is required to use
``django-contact-form``. First, you'll need to make sure you've
specified the appropriate settings for `Django to send email
<https://docs.djangoproject.com/en/dev/topics/email/>`_. Most
commonly, this will be ``EMAIL_HOST``, ``EMAIL_PORT``,
``EMAIL_HOST_USER`` and ``EMAIL_HOST_PASSWORD``.

You'll also want to make sure ``django-contact-form`` sends mail from
the correct address, and sends to the correct address(es). Two
standard Django settings control this:

* By default, the ``From:`` header of all emails sent by
  ``django-contact-form`` will be whatever email address is specified
  in ``DEFAULT_FROM_EMAIL``.

* By default, the recipient list for emails sent by
  ``django-contact-form`` will be the email addresses specified in
  ``MANAGERS``.

If you'd prefer something else, this behavior is configurable; see
:ref:`the form documentation <forms>` for details on how to customize
the email addresses used.


Templates
~~~~~~~~~

The following templates are required by the default setup of
``django-contact-form``, so you'll need to create them:

* ``contact_form/contact_form.html`` is the template which actually
  renders the contact form. Important context variables are:

  ``form``
    The contact form instance.

* ``contact_form/contact_form_sent.html`` is the template rendered
  after a message is successfully sent through the contact form. It
  has no specific context variables, beyond whatever's supplied by the
  context processors in use on your site.

Additionally, the generated email makes use of two templates:
``contact_form/contact_form_subject.txt`` will be rendered to obtain
the subject line, and ``contact_form/contact_form.txt`` will be
rendered to obtain the body of the email. These templates use
``RequestContext``, so any context processors will be applied, and
have the following additional context:

``site``
    The current site. Either a ``Site`` instance if
    ``django.contrib.sites`` is installed, or a ``RequestSite``
    instance if not.

``body``
    The body of the message the user entered into the contact form.

``email``
    The email address the user supplied to the contact form.

``name``
    The name the user supplied to the contact form.


URL configuration
~~~~~~~~~~~~~~~~~

Once you've got settings and templates set up, all that's left is to
configure your URLs to point to the ``django-contact-form`` views. A
URLconf -- ``contact_form.urls`` -- is provided with
``django-contact-form``, which will wire up these views with default
behavior; to make use of it, simply include it at whatever point in
your URL hierarchy you'd like your contact form to live. For example,
to place it at ``/contact/``:

.. code-block:: python

    url(r'^contact/', include('contact_form.urls')),
