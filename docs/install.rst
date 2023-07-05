.. _install:


Installation and recommended configuration
==========================================

django-contact-form |release| supports Django 3.2, 4.1, and 4.2 on Python 3.8,
3.9, 3.10, and 3.11 (Django 4.1 and 4.2 only). Note that Django 3.2's support
for Python 3.10 was added in Django 3.2.9, so you may experience issues with
Python 3.10 and earlier Django 3.2 versions.

.. note:: **Django 3.2 and supported Python versions**

   Django 3.2 was released before Python 3.10 had come out, and although it now
   supports Python 3.10, it did not officially do so until the Django 3.2.9
   release. You may encounter problems if you try to use Django 3.2.8 or
   earlier with Python 3.10.

   Also, although Django 3.2 continues to officially support Python 3.6 and
   3.7, django-contact-form |release| does not, because the Python core team's
   support windows for Python 3.6 and 3.7 have ended.


Installing django-contact-form
------------------------------

To install django-contact-form, run the following command from a command
prompt/terminal:

.. tab:: macOS/Linux/other Unix

   .. code-block:: shell

      python -m pip install django-contact-form

.. tab:: Windows

   .. code-block:: shell

      py -m pip install django-contact-form

If you plan to use the spam-filtering
:class:`~django_contact_form.forms.AkismetContactForm`, you will also need the
``akismet`` Python library. You can install this separately, or you can have it
automatically installed for you alongside django-contact-form, by instead
running:

.. tab:: macOS/Linux/other Unix

   .. code-block:: shell

      python -m pip install django-contact-form[akismet]

.. tab:: Windows

   .. code-block:: shell

      py -m pip install django-contact-form[akismet]

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
``pip`` to install django-contact-form will also install the latest
supported version of Django.

Installing from a source checkout
---------------------------------

If you want to work on django-contact-form, you can obtain a source checkout.

The development repository for django-contact-form is at
<https://github.com/ubernostrum/django-contact-form>. If you have git
installed, you can obtain a copy of the repository by typing:

.. code-block:: shell

   git clone https://github.com/ubernostrum/django-contact-form.git

From there, you can use git commands to check out the specific revision you
want, and perform an “editable” install (allowing you to change code as you
work on it) by typing:

.. tab:: macOS/Linux/other Unix

   .. code-block:: shell

      python -m pip install -e .

.. tab:: Windows

   .. code-block:: shell

      py -m pip install -e .

Next steps
----------

To get up and running quickly, check out :ref:`the quick start guide
<quickstart>`. For full documentation, see :ref:`the documentation
index <index>`.
