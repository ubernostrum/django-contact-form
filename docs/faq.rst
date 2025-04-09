.. _faq:


Frequently asked questions
==========================

The following notes answer some common questions, and may be useful to you when
installing, configuring or using django-contact-form.


What versions of Django and Python are supported?
-------------------------------------------------

``django-contact-form`` |release| supports Django 4.2, 5.1, and 5.2, and Python
3.9 through 3.13. See `Django's Python support matrix
<https://docs.djangoproject.com/en/dev/faq/install/#what-python-version-can-i-use-with-django>`_
for details of which Python versions are compatible with each version of
Django.


What license is ``django-contact-form`` under?
----------------------------------------------

``django-contact-form`` is offered under a three-clause BSD-style license; this
is `an OSI-approved open-source license
<http://www.opensource.org/licenses/bsd-license.php>`_, and allows you a large
degree of freedom in modifying and redistributing the code. For the full terms,
see the file `LICENSE` which came with your copy of ``django-contact-form``; if
you did not receive a copy of this file, you can view it online at
<https://github.com/ubernostrum/django-contact-form/blob/trunk/LICENSE>.


Why aren't there any default templates?
---------------------------------------

Usable default templates, for a Django application designed to be widely
reused, are essentially impossible to produce; variations in site design, block
structure, etc. cannot be reliably accounted for. As such,
``django-contact-form`` provides bare-bones (i.e., containing no HTML structure
whatsoever) templates in its source distribution to enable running tests, and
otherwise just provides good documentation of all required templates and the
context made available to them.


Why am I getting a bunch of ``BadHeaderError`` exceptions?
----------------------------------------------------------

Most likely, you have an error in your
:class:`~django_contact_form.forms.ContactForm` subclass. Specifically, one or
more of :attr:`~django_contact_form.forms.ContactForm.from_email`,
:attr:`~django_contact_form.forms.ContactForm.recipient_list` or
:meth:`~django_contact_form.forms.ContactForm.subject` are returning values
which contain newlines.

As a security precaution against `email header injection attacks
<https://en.wikipedia.org/wiki/Email_injection>`_ (which allow spammers and
other malicious users to manipulate email and potentially cause automated
systems to send mail to unintended recipients), `Django's email-sending
framework does not permit newlines in message headers
<https://docs.djangoproject.com/en/stable/topics/email/#preventing-header-injection>`_.
:exc:`~django.core.mail.BadHeaderError` is the exception Django raises when a
newline is detected in a header. By default,
:meth:`~django_contact_form.forms.ContactForm.subject` will forcibly condense
the subject to a single line.

Note that this only applies to the headers of an email message; the message
body can (and usually does) contain newlines.


I found a bug or want to make an improvement!
---------------------------------------------

The canonical development repository for ``django-contact-form`` is online at
<https://github.com/ubernostrum/django-contact-form>. Issues and pull requests
can both be filed there.

If you'd like to contribute to ``django-contact-form``, that's great!  Just
please remember that pull requests should include tests and documentation for
any changes made, and that following `PEP 8
<https://www.python.org/dev/peps/pep-0008/>`_ is mandatory. Pull requests
without documentation won't be merged, and PEP 8 style violations or test
coverage below 100% are both configured to break the build.
