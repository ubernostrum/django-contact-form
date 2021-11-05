.. _install:


Installation guide
==================

The |release| release of django-contact-form supports Django 2.2, 3.1,
3.2, and 4.0 on Python 3.6, 3.7, 3.8, and 3.9.


Normal installation
-------------------

The preferred method of installing django-contact-form is via `pip`,
the standard Python package-installation tool. If you don't have
`pip`, instructions are available for `how to obtain and install it
<https://pip.pypa.io/en/latest/installing.html>`_. If you're using a
supported version of Python, `pip` should have come bundled with your
installation of Python.

Once you have `pip`, type::

    pip install django-contact-form

If you plan to use the included spam-filtering contact form class,
:class:`~contact_form.forms.AkismetContactForm`, you will also need
`the Python akismet module <https://pypi.org/project/akismet/>`_. You
can manually install it via `pip install akismet`, or tell
django-contact-form to install it for you, by running::

    pip install django-contact-form[akismet]

If you don't have a copy of a compatible version of Django, installing
django-contact-form will also automatically install one for you.


Installing from a source checkout
---------------------------------

If you want to work on django-contact-form, you can obtain a source
checkout.

The development repository for django-contact-form is at
<https://github.com/ubernostrum/django-contact-form>. If you have `git
<http://git-scm.com/>`_ installed, you can obtain a copy of the
repository by typing::

    git clone https://github.com/ubernostrum/django-contact-form.git

From there, you can use git commands to check out the specific
revision you want, and perform an "editable" install (allowing you to
change code as you work on it) by typing::

    pip install -e .


Next steps
----------

To get up and running quickly, check out :ref:`the quick start guide
<quickstart>`. For full documentation, see :ref:`the documentation
index <index>`.
