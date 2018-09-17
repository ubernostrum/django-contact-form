.. _views:
.. module:: contact_form.views


Built-in views
==============

.. class:: ContactFormView

    The base view class from which most custom contact-form views
    should inherit. If you don't need any custom functionality, and
    are content with the default
    :class:`~contact_form.forms.ContactForm` class, you can also use
    it as-is (and the provided URLConf, `contact_form.urls`, does
    exactly this).

    This is a subclass of Django's
    :class:`~django.views.generic.edit.FormView`, so refer to the
    Django documentation for a list of attributes/methods which can be
    overridden to customize behavior.

    One non-standard attribute is defined here:

    .. attribute:: recipient_list

       The list of email addresses to send mail to. If not specified,
       defaults to the
       :attr:`~contact_form.forms.ContactForm.recipient_list` of the
       form.

    Additionally, the following standard (from
    :class:`~django.views.generic.edit.FormView`) methods and
    attributes are commonly useful to override (all attributes below
    can also be passed to
    :meth:`~django.views.generic.base.View.as_view()` in the URLconf,
    permitting customization without the need to write a full custom
    subclass of :class:`ContactFormView`):

    .. attribute:: form_class

       The form class to use. By default, will be
       :class:`~contact_form.forms.ContactForm`. This can also be
       overridden as a method named
       :meth:`~django.views.generic.edit.FormMixin.form_class`; this
       permits, for example, per-request customization (by inspecting
       attributes of `self.request`).

    .. attribute:: template_name

       A :class:`str`, the template to use when rendering the form. By
       default, will be `contact_form/contact_form.html`.

    .. method:: get_success_url

       The URL to redirect to after successful form submission. Can be
       a hard-coded string, the string resulting from calling Django's
       :func:`~django.urls.reverse` helper, or the lazy object
       produced by Django's :func:`~django.urls.reverse_lazy`
       helper. Default value is the result of calling
       :func:`~django.urls.reverse_lazy` with the URL name
       `'contact_form_sent'`.

       :rtype: str
       
    .. method:: get_form_kwargs

       Returns additional keyword arguments (as a dictionary) to pass
       to the form class on initialization.

       By default, this will return a dictionary containing the
       current :class:`~django.http.HttpRequest` (as the key
       `request`) and, if :attr:`~ContactFormView.recipient_list` was
       defined, its value (as the key `recipient_list`).

       .. warning:: If you override :meth:`get_form_kwargs`, you
          **must** ensure that, at the very least, the keyword
          argument `request` is still provided, or
          :class:`~contact_form.forms.ContactForm` initialization will
          raise :exc:`TypeError`. The easiest approach is to use
          :func:`super` to call the base implementation in
          :class:`ContactFormView`, and modify the dictionary it
          returns.

       :rtype: dict
