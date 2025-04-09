.. _install:


Installation guide
==================

``django-contact-form`` |release| supports Django 4.2, 5.1, and 5.2, and Python
3.9 through 3.13. See `Django's Python support matrix
<https://docs.djangoproject.com/en/dev/faq/install/#what-python-version-can-i-use-with-django>`_
for details of which Python versions are compatible with each version of
Django.


Installing ``django-contact-form``
----------------------------------

To install ``django-contact-form``, run the following command from a command
prompt/terminal:

.. tab:: macOS/Linux/other Unix

   .. code-block:: shell

      python -m pip install django-contact-form

.. tab:: Windows

   .. code-block:: shell

      py -m pip install django-contact-form

If you plan to use the spam-filtering
:class:`~django_contact_form.forms.AkismetContactForm`, you will also need `the
Python akismet client <https://akismet.readthedocs.io/>`_. You can install this
separately (in which case, be sure to install at least version 24.5.0 of
``akismet``), or you can have it automatically installed for you alongside
``django-contact-form``, by running:

.. tab:: macOS/Linux/other Unix

   .. code-block:: shell

      python -m pip install "django-contact-form[akismet]"

.. tab:: Windows

   .. code-block:: shell

      py -m pip install "django-contact-form[akismet]"

This will use ``pip``, the standard Python package-installation tool. If you
are using a supported version of Python, your installation of Python should
have come with ``pip`` bundled. If ``pip`` does not appear to be present, you
can try running the following from a command prompt/terminal:

.. tab:: macOS/Linux/other Unix

   .. code-block:: shell

      python -m ensurepip --upgrade

.. tab:: Windows

   .. code-block:: shell

      py -m ensurepip --upgrade

Instructions are also available for `how to obtain and manually install or
upgrade pip <https://pip.pypa.io/en/latest/installation/>`_.

If you don't already have a supported version of Django installed, using
``pip`` to install ``django-contact-form`` will also install the latest
supported version of Django.


Installing for local development
--------------------------------

If you want to work on ``django-contact-form``, you can obtain a source
checkout.

The development repository for ``django-contact-form`` is at
<https://github.com/ubernostrum/django-contact-form>. If you have `git
<http://git-scm.com/>`_ installed, you can obtain a copy of the repository by
typing::

    git clone https://github.com/ubernostrum/django-contact-form.git

Then follow the instructions in the file ``CONTRIBUTING.rst`` in the root
directory of the source checkout.


Next steps
----------

To start using ``django-contact-form``, check out :ref:`the usage guide
<usage>`.
