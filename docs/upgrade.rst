.. _upgrade:

Upgrading from previous versions
================================

The current release series of django-contact-form is the 2.x series,
which is not backwards-compatible with the django-contact-form 1.x
release series.


Changes between django-contact-form 1.x and 2.x
-----------------------------------------------


Module renaming
~~~~~~~~~~~~~~~

Prior to 2.x, django-contact-form installed a Python module named
`contact_form`. To avoid silent incompatibilities, and to conform to
more recent best practices, django-contact-form 2.x now installs a
module named `django_contact_form`. Attempts to import from the
`registration` module will immediately fail with :exc:`ImportError`.

Many installations will be able to adapt by replacing references to
`registration` with references to `django_contact_form`.


Template directory renamed
~~~~~~~~~~~~~~~~~~~~~~~~~~

Similar to the module renaming above, the name of the default
directory in which django-contact-form looks for templates has changed
from `contact_form/` to `django_contact_form/`.


.. _renamed-get-context:

Method renamed: get_context() -> get_message_context()
``````````````````````````````````````````````````````

Prior to 2.x, :class:`~django_contact_form.forms.ContactForm` provided
a method named `get_context()` which was used to generate the template
context from which the message would be rendered. However, Django 4.0
introduced `a new template-based system for rendering forms
<https://docs.djangoproject.com/en/stable/releases/4.0/#template-based-form-rendering>`_,
and as a result :class:`django.forms.Form` now has a method named
:meth:`~django.forms.Form.get_context`.

To resolve this conflict with Django's own base form class, the method
in django-contact-form has been renamed to
:meth:`~django_contact_form.forms.ContactForm.get_message_context`,
which hopefully will not be adopted by any future version of Django's
own forms system.

If you were previously overriding `get_context()`, you should rename
your overridden method to
:meth:`~django_contact_form.forms.ContactForm.get_message_context` to
ensure it is still called properly. If you have other code which
called `get_context()`, you should update any such references to call
:meth:`~django_contact_form.forms.ContactForm.get_message_context`
instead.