.. module:: contact_form.views


Built-in views
==============

.. class:: ContactFormView

    The base view class from which most custom contact-form views
    should inherit. If you don't need any custom functionality, and
    are content with the default
    :class:`~contact_form.forms.ContactForm` class, you can also just
    use it as-is (and the provided URLConf, ``contact_form.urls``,
    does exactly this).

    This is a subclass of `Django's FormView
    <https://docs.djangoproject.com/en/dev/ref/class-based-views/flattened-index/#formview>`_,
    so refer to the Django documentation for a list of
    attributes/methods which can be overridden to customize behavior.

    By default, ``success_url`` will be the named URL
    ``contact_form_sent``; this URL needs to exist and should resolve
    properly. In the default URLConf, that URL is a ``TemplateView``
    rendering the template ``contact_form/contact_form_sent.html``.