.. _faq:


Frequently asked questions
==========================

The following notes answer some common questions, and may be useful to
you when installing, configuring or using django-contact-form.


What versions of Django are supported?
--------------------------------------

As of django-contact-form |version|, Django 1.4 and 1.5 are
supported. It is expected that django-contact-form |version| will also
work unmodified with Django 1.6, once Django 1.6 is released.

Django 1.3 may also work, but is unsupported. Django 1.2 and earlier
will not work with django-contact-form |version|.


What versions of Python are supported?
--------------------------------------

On Django 1.4 and 1.5, django-contact-form |version| supports Python
2.6 and 2.7. On Django 1.5, Python 3.3 is also supported.


Why aren't there any default templates I can use?
-------------------------------------------------

Usable default templates, for an application designed to be widely
reused, are essentially impossible to produce; variations in site
design, block structure, etc. cannot be reliably accounted for. As
such, django-contact-form simply provides good documentation of all
templates it requires and the context made available to them.


What happened to the spam-filtering form in previous versions?
--------------------------------------------------------------

Older versions of django-contact-form shipped a subclass of
:class:`~contact_form.forms.ContactForm` which used `the Akismet web
service <http://akismet.com/>`_ to identify and reject spam
submissions.

Unfortunately, the Akismet Python library -- required in order to use
such a class -- does not currently support all versions of Python on
which django-contact-form is supported, meaning it cannot be included
in django-contact-form by default.


Why am I getting a bunch of BadHeaderError exceptions?
------------------------------------------------------

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