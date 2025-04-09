.. _changelog:

Changelog
=========

This is a list of changes made in released versions of ``django-contact-form``
over time.


Version numbering
-----------------

``django-contact-form`` uses "DjangoVer", a version number system based on the
corresponding supported Django versions. The format of a
``django-contact-form`` version number is ``A.B.C``, where ``A.B`` is the
version number of the latest Django feature release supported by that version
of ``django-contact-form``, and ``C`` is an incrementing value for releases of
``django-contact-form`` paired to that Django feature release.

The policy of ``django-contact-form`` is to support the Django feature release
indicated in the version number, along with any other lower-numbered Django
feature releases receiving support from the Django project at the time of
release.

For example, consider a hypothetical ``django-contact-form`` version
5.0.2. This indicates that the most recent supported Django feature release is
5.0, and that it is the third release of ``django-contact-form`` to support
Django 5.0 (after 5.0.0 and 5.0.1). Since the Django project at the time was
supporting Django 5.0 and 4.2, that version of ``django-contact-form`` would
also support Django 5.0 and 4.2.


API stability and deprecations
------------------------------

The API stability/deprecation policy for ``django-contact-form`` is as follows:

* The supported stable public API is the set of symbols which are documented in
  this documentation. For classes, the supported stable public API is the set
  of methods and attributes of those classes whose names do not begin with one
  or more underscore (``_``) characters and which are documented in this
  documentation.

* When a public API is to be removed, or undergo a backwards-incompatible
  change, it will emit a deprecation warning which serves as notice of the
  intended removal or change. This warning will be emitted for at least two
  releases, after which the removal or change may occur without further
  warning. This is different from Django's own deprecation policy, which avoids
  completing a removal/change in "LTS"-designated releases. Since
  ``django-contact-form`` does not have "LTS" releases, it does not need that
  exception.

* Security fixes, and fixes for high-severity bugs (such as those which might
  cause unrecoverable crash or data loss), are not required to emit deprecation
  warnings, and may -- if needed -- impose backwards-incompatible change in any
  release. If this occurs, this changelog document will contain a note
  explaining why the usual deprecation process could not be followed for that
  case.

* This policy is in effect as of the adoption of "DjangoVer" versioning, with
  version 5.0.0 of ``django-contact-form``.


Releases under DjangoVer
------------------------

Version 5.2.0
~~~~~~~~~~~~~

Released April 2025

* Supported Django versions are now 4.2, 5.1, and 5.2.

Version 5.1.2
~~~~~~~~~~~~~

Released March 2025

* Fixed a bug with the Akismet integration where the first call to create an
  Akismet client would succeed in creating and returning it, but subsequent
  calls would not return the cached client instance. Now subsequent calls do
  correctly return the cached instance.

Version 5.1.1
~~~~~~~~~~~~~

Released November 2024

* Supported Python versions are now 3.9, 3.10, 3.11, 3.12, and 3.13.

Version 5.1.0
~~~~~~~~~~~~~

Released August 2024

* Supported Django versions are now 4.2, 5.0, and 5.1.


Version 5.0.1
~~~~~~~~~~~~~

Released May 2024

* Correct an issue in the changelog for 5.0.0.

* Correct an issue with the display of the package's documentation/source URLs
  on the Python Package Index.


Version 5.0.0
~~~~~~~~~~~~~

Released May 2024

* Adopted "DjangoVer" versioning.

* The :class:`~django_contact_form.forms.AkismetContactForm` and its Akismet
  integration have been rewritten to make use of more recent versions of the
  Python Akismet client. Configuring the Akismet client via Django settings is
  now deprecated, and support for configuring via Django settings will be
  removed in a future version of ``django-contact-form``. The
  ``AkismetContactForm`` class now also provides two overridable public methods
  to allow customization of the Akismet API client instance and the arguments
  passed to the Akismet spam check.


Releases not under DjangoVer
----------------------------

Version 2.1
~~~~~~~~~~~

Released July 2023

* The supported Django versions are now 3.2, 4.1, and 4.2.


Version 2.0.1
~~~~~~~~~~~~~

Released May 2022

* Corrected several issues in the documentation of the 2.0 release.


Version 2.0
~~~~~~~~~~~

Released May 2022

Major version bump, with several changes:

* The supported Django versions are 3.2 and 4.0.

* Prior to 2.x, django-contact-form installed a Python module named
  ``contact_form``. To avoid silent incompatibilities, and to conform to more
  recent best practices, django-contact-form 2.x now installs a module named
  ``django_contact_form``. Attempts to import from the ``contact_form`` module
  will immediately fail with :exc:`ImportError`. Many installations will be
  able to adapt by replacing references to ``contact_form`` with references to
  ``django_contact_form``.

* Similar to the module renaming above, the name of the default directory in
  which django-contact-form looks for templates has changed from
  ``contact_form/`` to ``django_contact_form/``.

* Prior to 2.x, :class:`~django_contact_form.forms.ContactForm` provided a
  method named ``get_context()`` which was used to generate the template
  context from which the message would be rendered. However, Django 4.0
  introduced `a new template-based system for rendering forms
  <https://docs.djangoproject.com/en/stable/releases/4.0/#template-based-form-rendering>`_,
  and as a result :class:`django.forms.Form` now has a method named
  :meth:`~django.forms.Form.get_context`. To resolve this conflict with
  Django's own base form class, the method in django-contact-form has been
  renamed to
  :meth:`~django_contact_form.forms.ContactForm.get_message_context`, which
  hopefully will not be adopted by any future version of Django's own forms
  system. If you were previously overriding ``get_context()``, you should
  rename your overridden method to
  :meth:`~django_contact_form.forms.ContactForm.get_message_context` to ensure
  it is still called properly. If you have other code which called
  ``get_context()``, you should update any such references to call
  :meth:`~django_contact_form.forms.ContactForm.get_message_context` instead.


Pre-2.0 versions
~~~~~~~~~~~~~~~~

``django-contact-form`` 1.0 was released in August 2013. Between that release
and 2.0 in 2022, no new features were added to ``django-contact-form``, and
releases were concerned solely with ensuring and documenting support for new
Django releases.
