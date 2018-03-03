.. _install:


Installation guide
==================

The |release| release of django-contact-form supports Django 1.11 and
2.0 on the following Python versions (matching the versions supported
by Django itself):

* Django 1.11 supports Python 2.7, 3.4, 3.5, and 3.6.

* Django 2.0 supports Python 3.4, 3.5, and 3.6.


Normal installation
-------------------

The preferred method of installing django-contact-form is via ``pip``,
the standard Python package-installation tool. If you don't have
``pip``, instructions are available for `how to obtain and install it
<https://pip.pypa.io/en/latest/installing.html>`_. If you're using
Python 2.7.9 or later (for Python 2) or Python 3.4 or later (for
Python 3), ``pip`` came bundled with your installation of Python.

Once you have ``pip``, type::

    pip install django-contact-form

If you plan to use the included spam-filtering contact form class,
:class:`~contact_form.forms.AkismetContactForm`, you will also need
the Python ``akismet`` module. You can manually install it via ``pip
install akismet``, or tell ``django-contact-form`` to install it for
you, by running::

    pip install django-contact-form[akismet]

If you do not already have a supported version of Django installed,
installing django-contact-form will automatically install the most
recent supported version of Django.


Installing from a source checkout
---------------------------------

If you want to work on django-contact-form, you can obtain a source
checkout.

The development repository for django-contact-form is at
<https://github.com/ubernostrum/django-contact-form>. If you have `git
<http://git-scm.com/>`_ installed, you can obtain a copy of the
repository by typing::

    git clone https://github.com/ubernostrum/django-contact-form.git

From there, you can use normal git commands to check out the specific
revision you want, and install it using ``pip install -e .`` (the
``-e`` flag specifies an "editable" install, allowing you to change
code as you work on django-contact-form, and have your changes picked
up automatically).


Configuration and use
---------------------

Once you have Django and django-contact-form installed, check out
:ref:`the quick start guide <quickstart>` to see how to get your
contact form up and running.