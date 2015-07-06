.. _faq:


Frequently asked questions
==========================

The following notes answer some common questions, and may be useful to
you when installing, configuring or using ``django-contact-form``.


What versions of Django are supported?
--------------------------------------

As of ``django-contact-form`` |version|, Django 1.7 and 1.8 are
supported.


What versions of Python are supported?
--------------------------------------

As of |version|, ``django-contact-form`` supports Python 2.7, 3.3, and
3.4. It is anticipated that when Python 3.5 is released,
``django-contact-form`` |version| will be compatible with it.


Why aren't there any default templates I can use?
-------------------------------------------------

Usable default templates, for an application designed to be widely
reused, are essentially impossible to produce; variations in site
design, block structure, etc. cannot be reliably accounted for. As
such, ``django-contact-form`` provides bare-bones (i.e., containing no
HTML structure whatsoever) templates in its source distribution to
enable running tests, and otherwise simply provides good documentation
of all required templates and the context made available to them.


What happened to the spam-filtering form in previous versions?
--------------------------------------------------------------

Older versions of ``django-contact-form`` shipped a subclass of
:class:`~contact_form.forms.ContactForm` which used `the Akismet web
service <http://akismet.com/>`_ to identify and reject spam
submissions.

Unfortunately, the Akismet Python library -- required in order to use
such a class -- does not currently support all versions of Python on
which ``django-contact-form`` is supported, meaning it cannot be
included in ``django-contact-form`` by default. The author of
``django-contact-form`` is working on producing a version of the
Akismet library compatible with Python 3, but it was not yet ready as
of the release of ``django-contact-form`` |version|.


Why am I getting a bunch of ``BadHeaderError`` exceptions?
----------------------------------------------------------

Most likely, you have an error in your
:class:`~contact_form.forms.ContactForm` subclass. Specifically, one
or more of :attr:`~contact_form.forms.ContactForm.from_email`,
:attr:`~contact_form.forms.ContactForm.recipient_list` or
:meth:`~contact_form.forms.ContactForm.subject` are returning values
which contain newlines.

As a security precaution against email header injection attacks (which
allow spammers and other malicious users to manipulate email and
potentially cause automated systems to send mail to unintended
recipients), `Django's email-sending framework does not permit
newlines in message headers
<https://docs.djangoproject.com/en/dev/topics/email/#preventing-header-injection>`_. ``BadHeaderError``
is the exception Django raises when a newline is detected in a header.

Note that this only applies to the headers of an email message; the
message body can (and usually does) contain newlines.