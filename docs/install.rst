.. _install:


Installation guide
==================

``django-contact-form`` |release| supports Django 4.2 and 5.0 on Python 3.8
(Django 4.2 only), 3.9 (Django 4.2 only), 3.10, 3.11, and 3.12.

Django 4.2 only added Python 3.12 support in the 4.2.8 release, so it is
suggested that you use at least Django 4.2.8 (and always recommended to use the
latest bugfix release of whichever Django version you choose to use).


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

Installing from a source checkout
---------------------------------

If you want to work on ``django-contact-form``, you can obtain a source
checkout.

The development repository for django-contact-form is at
<https://github.com/ubernostrum/django-contact-form>. If you have git
installed, you can obtain a copy of the repository by typing:

.. code-block:: shell

   git clone https://github.com/ubernostrum/django-contact-form.git

From there, you can use git commands to check out the specific revision you
want, and perform an "editable" install (allowing you to change code as you
work on it) by typing:

.. tab:: macOS/Linux/other Unix

   .. code-block:: shell

      python -m pip install -e .

.. tab:: Windows

   .. code-block:: shell

      py -m pip install -e .

Next steps
----------

To start using ``django-contact-form``, check out :ref:`the usage guide
<usage>`.
