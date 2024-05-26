.. _forms:
.. module:: django_contact_form.forms

Contact form classes
====================

There are two contact-form classes included in django-contact-form;
one provides all the infrastructure for a contact form, and will
usually be the base class for subclasses which want to extend or
modify functionality. The other is a subclass which adds spam
filtering to the contact form.


The base contact form class
---------------------------

.. autoclass:: ContactForm


The spam-filtering contact form class
-------------------------------------

.. autoclass:: AkismetContactForm
