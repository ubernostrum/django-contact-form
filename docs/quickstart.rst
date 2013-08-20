.. _quickstart:

Quick start guide
=================

Before installing django-contact-form, you'll need to have a copy of
`Django <http://www.djangoproject.com>`_ already installed. For the
|version| release, Django 1.4 or newer is required.

For further information, consult the `Django download page
<http://www.djangoproject.com/download/>`_, which offers convenient
packaged downloads and installation instructions.


Installing django-contact-form
------------------------------

There are several ways to install django-contact-form:

* Automatically, via a package manager.

* Manually, by downloading a copy of the release package and
  installing it yourself.

* Manually, by performing a Mercurial checkout of the latest code.

It is also highly recommended that you learn to use `virtualenv
<http://pypi.python.org/pypi/virtualenv>`_ for development and
deployment of Python software; ``virtualenv`` provides isolated Python
environments into which collections of software (e.g., a copy of
Django, and the necessary settings and applications for deploying a
site) can be installed, without conflicting with other installed
software. This makes installation, testing, management and deployment
far simpler than traditional site-wide installation of Python
packages.


Automatic installation via a package manager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Several automatic package-installation tools are available for Python;
the recommended one is `pip <https://pypi.python.org/pypi/pip>`_.

Using ``pip``, type::

    pip install django-contact-form

It is also possible that your operating system distributor provides a
packaged version of django-contact-form. Consult your operating
system's package list for details, but be aware that third-party
distributions may be providing older versions of django-contact-form,
and so you should consult the documentation which comes with your
operating system's package.


Manual installation from a downloaded package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you prefer not to use an automated package installer, you can
download a copy of django-contact-form and install it manually. The
latest release package can be downloaded from `django-contact-form's
listing on the Python Package Index
<http://pypi.python.org/pypi/django-contact-form/>`_.

Once you've downloaded the package, unpack it (on most operating
systems, simply double-click; alternately, type ``tar zxvf
django-contact-form-1.0.tar.gz`` at a command line on Linux, Mac OS X
or other Unix-like systems). This will create the directory
``django-contact-form-1.0``, which contains the ``setup.py``
installation script. From a command line in that directory, type::

    python setup.py install

Note that on some systems you may need to execute this with
administrative privileges (e.g., ``sudo python setup.py install``).


Manual installation from a Mercurial checkout
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you'd like to try out the latest in-development code, you can
obtain it from the django-contact-form repository, which is hosted at
`Bitbucket <http://bitbucket.org/>`_ and uses `Mercurial
<http://mercurial.selenic.com/wiki/>`_ for version control. To obtain
the latest code and documentation, you'll need to have Mercurial
installed, at which point you can type::

    hg clone http://bitbucket.org/ubernostrum/django-contact-form/

You can also obtain a copy of a particular release of
django-contact-form by specifying the ``-r`` argument to ``hg clone``;
each release is given a tag of the form ``vX.Y``, where "X.Y" is the
release number. So, for example, to check out a copy of the |version|
release, type::

    hg clone -r v1.0 http://bitbucket.org/ubernostrum/django-contact-form/

In either case, this will create a copy of the django-contact-form
Mercurial repository on your computer; you can then add the
``django-contact-form`` directory inside the checkout your Python
import path, or use the ``setup.py`` script to install as a package.


Basic configuration and use
---------------------------

Once installed, only a small amount of setup is required to use
django-contact-form. First, you'll need to make sure you've specified
the appropriate settings for `Django to send email
<https://docs.djangoproject.com/en/dev/topics/email/>`_. Most
commonly, this will be ``EMAIL_HOST``, ``EMAIL_PORT``,
``EMAIL_HOST_USER`` and ``EMAIL_HOST_PASSWORD``.

You'll also want to make sure django-contact-form sends mail from the
correct address, and sends to the correct address(es). Two standard
Django settings control this:

* By default, the ``From:`` header of all emails sent by
  django-contact-form will be whatever email address is specified in
  ``DEFAULT_FROM_EMAIL``.

* By default, the recipient list for emails sent by
  django-contact-form will be the email addresses specified in
  ``MANAGERS``.

If you'd prefer something else, this behavior is configurable; see
:ref:`the form documentation <forms>` for details on how to customize
the email addresses used.


Templates
~~~~~~~~~

The following templates are required by the default setup of
django-contact-form, so you'll need to create them:

* ``contact_form/contact_form.html`` is the template which actually
  renders the contact form. Important context variables are:

  ``form``
    The contact form instance.

* ``contact_form/contact_form_sent.html`` is the template rendered
  after a message is successfully sent through the contact form. It
  has no specific context variables, beyond whatever's supplied by the
  context processors in use.

Additionally, the generated email makes use of two templates:
``contact_form/contact_form_subject.txt`` will be rendered to obtain
the subject line, and ``contact_form/contact_form.txt`` will be
rendered to obtain the body of the email. These templates use
``RequestContext``, so any context processors will be applied, and
have the following additional context:

``site``
    The current site, either a ``Site`` instance if
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
configure your URLs to point to the django-contact-form views. A
URLConf -- ``contact_form.urls`` -- is provided wich
django-contact-form, which will wire up these views with default
behavior; to make use of it, simply include it at whatever point in
your URL hierarchy you'd like your contact form to live. For example,
to place it at ``/contact/``:

.. code-block:: python

    (r'^contact/', include('contact_form.urls')),
