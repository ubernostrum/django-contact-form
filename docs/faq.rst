.. _faq:


Frequently asked questions
==========================

The following notes answer some common questions, and may be useful to
you when installing, configuring or using django-contact-form.


What versions of Django and Python are supported?
-------------------------------------------------

As of django-contact-form |release|, Django 1.8, 1.10, and 1.11 are
supported, on Python 2.7, 3.3, (Django 1.8 only), 3.4, 3.5, or 3.6
(Django 1.11 only). Although Django 1.8 supported Python 3.2 at
initial release, Python 3.2 is now at its end-of-life and
django-contact-form no longer supports it.


What license is django-contact-form under?
----------------------------------------------

django-contact-form is offered under a three-clause BSD-style
license; this is `an OSI-approved open-source license
<http://www.opensource.org/licenses/bsd-license.php>`_, and allows you
a large degree of freedom in modifiying and redistributing the
code. For the full terms, see the file ``LICENSE`` which came with
your copy of django-contact-form; if you did not receive a copy of
this file, you can view it online at
<https://github.com/ubernostrum/django-contact-form/blob/master/LICENSE>.


Why aren't there any default templates I can use?
-------------------------------------------------

Usable default templates, for an application designed to be widely
reused, are essentially impossible to produce; variations in site
design, block structure, etc. cannot be reliably accounted for. As
such, django-contact-form provides bare-bones (i.e., containing no
HTML structure whatsoever) templates in its source distribution to
enable running tests, and otherwise just provides good documentation
of all required templates and the context made available to them.


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
<https://docs.djangoproject.com/en/1.11/topics/email/#preventing-header-injection>`_.
``BadHeaderError`` is the exception Django raises when a newline is
detected in a header.

Note that this only applies to the headers of an email message; the
message body can (and usually does) contain newlines.


I found a bug or want to make an improvement!
---------------------------------------------

The canonical development repository for django-contact-form is
online at <https://github.com/ubernostrum/django-contact-form>. Issues
and pull requests can both be filed there.

If you'd like to contribute to django-contact-form, that's great!
Just please remember that pull requests should include tests and
documentation for any changes made, and that following `PEP 8
<https://www.python.org/dev/peps/pep-0008/>`_ is mandatory. Pull
requests without documentation won't be merged, and PEP 8 style
violations or test coverage below 100% are both configured to break
the build.


I'm getting errors about "akismet" when trying to run tests?
------------------------------------------------------------

The full test suite of django-contact-form exercises all of its
functionality, including the spam-filtering
:class:`~contact_forms.forms.AkismetContactForm`. That class uses `the
Wordpress Akismet spam-detection service <https://akismet.com/>`_ to
perform spam filtering, and so requires the Python ``akismet`` module
to communicate with the Akismet service, and some additional
configuration (in the form of a valid Akismet API key and associated
URL).

By default, the tests for
:class:`~contact_forms.forms.AkismetContactForm` will be skipped
unless the required configuration (in the form of either a pair of
Django settings, or a pair of environment variables) is
detected. However, if you have supplied Akismet configuration but do
*not* have the Python ``akismet`` module, you will see test errors
from attempts to import ``akismet``. You can resolve this by running::

    pip install akismet

or (if you do not intend to use
:class:`~contact_forms.forms.AkismetContactForm`) by no longer
configuring the Django settings/environment variables used by Akismet.

Additionally, if the :class:`~contact_forms.forms.AkismetContactForm`
tests are skipped, the default code-coverage report will fail due to
the relevant code not being exercised during the test run.