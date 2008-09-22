=====================
Included form classes
=====================


Two form classes are included with this application; one,
``contact_form.forms.ContactForm`` implements the necessary base
functionality of a contact form, and other contact-form classes should
inherit from it to receive that functionality. The other,
contact_form.forms.AkismetContactForm``, is a subclass of
``ContactForm`` provided both because it is useful and as a
demonstration of subclassing ``ContactForm``.


``contact_form.forms.ContactForm``
==================================

Base contact form class from which all contact form classes should
inherit.

If you don't need any custom functionality, you can simply use this
form to provide basic contact functionality; it will collect name,
email address and message.

The ``contact_form`` view included in this application knows how to
work with this form and can handle many types of subclasses as well
(see below for a discussion of the important points), so in many cases
it will be all that you need. If you'd like to use this form or a
subclass of it from one of your own views, just do the following:

    1. When you instantiate the form, pass the current ``HttpRequest``
       object to the constructor as the keyword argument ``request``;
       this is used internally by the base implementation, and also
       made available so that subclasses can add functionality which
       relies on inspecting the request.
       
    2. To send the message, call the form's ``save`` method, which
       accepts the keyword argument ``fail_silently`` and defaults it
       to ``False``. This argument is passed directly to
       ``send_mail``, and allows you to suppress or raise exceptions
       as needed for debugging. The ``save`` method has no return
       value.
       
Other than that, treat it like any other form; validity checks and
validated data are handled normally, through the ``is_valid`` method
and the ``cleaned_data`` dictionary.


Base implementation
-------------------

Under the hood, this form uses a somewhat abstracted interface in
order to make it easier to subclass and add functionality. There are
several important attributes subclasses may want to look at
overriding, all of which will work (in the base implementation) as
either plain attributes or as callable methods:

    * ``from_email`` -- used to get the address to use in the
      ``From:`` header of the message. The base implementation returns
      the value of the ``DEFAULT_FROM_EMAIL`` setting.
      
    * ``message`` -- used to get the message body as a string. The
      base implementation renders a template using the form's
      ``cleaned_data`` dictionary as context.
      
    * ``recipient_list`` -- used to generate the list of recipients
      for the message. The base implementation returns the email
      addresses specified in the ``MANAGERS`` setting.
      
    * ``subject`` -- used to generate the subject line for the
      message. The base implementation returns the string 'Message
      sent through the web site', with the name of the current
      ``Site`` prepended.
      
    * ``template_name`` -- used by the base ``ContactForm`` class to
      determine which template to use for rendering the
      message. Default is ``contact_form/contact_form.txt``.
    
    * ``subject_template_name`` -- used by the base ``ContactForm``
      class to determine which template to use for rendering the
      message's subject line. Regardless of the output of rendering
      this template, it will be condensed to a single line of text;
      multi-line subjects are not permitted. Default is
      ``contact_form/contact_form_subject.txt``.
      
Internally, the base implementation ``_get_message_dict`` method
collects ``from_email``, ``message``, ``recipient_list`` and
``subject`` into a dictionary, which the ``save`` method then passes
directly to ``send_mail`` as keyword arguments.

Particularly important is the ``message`` attribute, with its base
implementation as a method which renders a template, and the
``subject`` attribute which defaults to a similar method; because they
pass ``cleaned_data`` as the template context, any additional fields
added by a subclass will automatically be available in the
template. This means that many useful subclasses can get by with just
adding a few fields and possibly overriding ``template_name`` and/or
``subject_template_name``.

Much useful functionality can be achieved in subclasses without having
to override much of the above; adding additional validation methods
works the same as any other form, and typically only a few items --
``recipient_list`` and ``subject_line``, for example, need to be
overridden to achieve customized behavior.


Other notes for subclassing
---------------------------

Subclasses which want to inspect the current ``HttpRequest`` to add
functionality can access it via the attribute ``request``; the base
``message`` and ``subject`` take advantage of this to use
``RequestContext`` when rendering their templates. See the
``AkismetContactForm`` subclass in this file for an example of using
the request to perform additional validation.

Subclasses which override ``__init__`` need to accept ``*args`` and
``**kwargs``, and pass them via ``super`` in order to ensure proper
behavior.

Subclasses should be careful if overriding ``_get_message_dict``,
since that method **must** return a dictionary suitable for passing
directly to ``send_mail`` (unless ``save`` is overridden as well).

Overriding ``save`` is relatively safe, though remember that code
which uses your form will expect ``save`` to accept the
``fail_silently`` keyword argument. In the base implementation, that
argument defaults to ``False``, on the assumption that it's far better
to notice errors than to silently not send mail from the contact form
(see also the Zen of Python: "Errors should never pass silently,
unless explicitly silenced").


``contact_form.forms.AkismetContactForm``
=========================================

Contact form which doesn't add any extra fields, but does add an
Akismet spam check to the validation routine.

Requires the setting ``AKISMET_API_KEY``, which should be a valid
Akismet API key.
