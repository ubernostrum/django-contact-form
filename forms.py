"""
A base contact form for allowing users to send email messages through
a web interface, and some subclasses demonstrating useful
functionality.

"""

import sha
from smtplib import SMTPException
from django import newforms as forms
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader, RequestContext
from django.contrib.sites.models import Site

# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary.
attrs_dict = { 'class': 'required' }


class ContactForm(forms.Form):
    """
    Base contact form class from which all contact form classes should
    inherit.
    
    If you don't need any custom functionality, you can simply use
    this form to provide basic contact functionality; it will collect
    name, email address and message.
    
    To add functionality, subclasses can override any or all of
    the following:

        * ``from_email`` -- used to get the address to use in the
          ``From:`` header of the message. The base implementation
          returns the value of the ``DEFAULT_FROM_EMAIL`` setting.
    
        * ``message`` -- used to get the message body as a string. The
          base implementation renders a template using the form's
          ``cleaned_data`` dictionary as context.
          
        * ``recipients`` -- used to generate the list of recipients
          for the message. The base implementation returns the email
          addresses specified in the ``MANAGERS`` setting.
          
        * ``subject`` -- used to generate the subject line for the
          message. The base implementation returns the string 'Message
          sent through the web site', with the name of the current
          ``Site`` prepended.
          
        * ``template_name`` -- used by the base ``message`` method
          to determine which template to use for rendering the
          message. Default is ``contact/contact_form.txt``
          
    Each of these can be a normal attribute or a method; the contact
    form view will handle either automatically.
          
    Subclasses which override ``__init__`` **must** accept ``*args``
    and ``**kwargs`` and pass them to the superclass ``__init__`` via
    ``super``.
    
    Subclasses which want to inspect the current ``HttpRequest`` to
    add functionality can access it via the attribute ``request``; the
    base ``get_message`` takes advantage of this to use
    ``RequestContext`` when rendering its template.

    Subclasses should also be careful when overriding ``save``, as
    this method is responsible for constructing and sending the actual
    email message.
    
    Beyond that, the sky's the limit; anything which is supported by
    Django's newforms can be added in a subclass. In most cases,
    however, subclasses will not need to override much, if anything,
    from the base form; for example, any additional fields defined in
    a subclass will be picked up and automatically passed to the
    template when the message is rendered, for example, so in many
    cases all that's needed is to change the value of
    ``template_name``, or override ``subject`` or ``recipients``.
    
    """
    def __init__(self, request, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.request = request
    
    name = forms.CharField(max_length=100,
                           widget=forms.TextInput(attrs=attrs_dict),
                           label=u'Your name')
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=200)),
                             label=u'Your email address')
    message = forms.CharField(widget=forms.Textarea(attrs=attrs_dict),
                              label=u'Your message')
    
    from_email = settings.DEFAULT_FROM_EMAIL
    
    recipients = [mail_tuple[1] for mail_tuple in settings.MANAGERS]
    
    subject = "[%s] Message sent through the web site" % Site.objects.get_current().name
    
    template_name = 'contact/contact_form.txt'
    
    def message(self):
        """
        Renders the body of the message to a string.
        
        """
        if callable(self.template_name):
            template_name = self.template_name()
        else:
            template_name = self.template_name
        t = loader.get_template(template_name)
        return t.render(RequestContext(self.request, self.cleaned_data))

    def save(self):
        """
        Builds and sends the email message.
        
        """
        if not self.is_valid():
            raise ValueError("Message cannot be sent from invalid contact form")
        message_dict = {}
        for message_part in ('from_email', 'message', 'recipients', 'subject'):
            attr = getattr(self, message_part)
            message_dict[message_part] = callable(attr) and attr() or attr
        try:
            send_mail(**message_dict))
        except SMTPException:
            return False
        return True


class AkismetContactForm(ContactForm):
    """
    Contact form which doesn't add any extra fields, but does add an
    Akismet spam check to the validation routine.
    
    Requires the setting ``AKISMET_API_KEY``, which should be a valid
    Akismet API key.
    
    """
    def clean_message(self):
        if hasattr(settings, 'AKISMET_API_KEY') and settings.AKISMET_API_KEY:
            from akismet import Akismet
            akismet_api = Akismet(key=settings.AKISMET_API_KEY,
                                  blog_url='http://%s/' % Site.objects.get_current().domain)
            if akismet_api.verify_key():
                akismet_data = { 'comment_type': 'comment',
                                 'referer': self.request.META.get('HTTP_REFERER', ''),
                                 'user_ip': self.request.META.get('REMOTE_ADDR', ''),,
                                 'user_agent': self.request.META.get('HTTP_USER_AGENT', '') }
                if akismet_api.comment_check(self.cleaned_data['message'], data=akismet_data, build_data=True):
                    raise forms.ValidationError(u"Akismet thinks this message is spam")
        return self.cleaned_data['message']


class CaptchaContactForm(ContactForm):
    """
    Extends the base contact form to add a simple CAPTCHA
    functionality for defeating automated spam bots.
    
    The CAPTCHA works by requiring a word to be typed into an extra
    field; a hidden field contains the SHA1 hash of this word and this
    site's ``SECRET_KEY`` setting, and will check that the word typed
    by the user hashes correctly.
    
    To set the word to use in the CAPTCHA, pass it to this form's
    constructor as the ``captcha`` keyword argument; the default if
    not supplied is "swordfish", but you really should pass in
    something else. Choosing a random word from a dictionary file is a
    good method.

    Note that because this form requires extra parameters passed to
    ``__init__``, you will need to write a custom view to use it.
    
    """
    def __init__(self, captcha_value="swordfish", *args, **kwargs):
        initial_data = { 'hash': sha.new(captcha_value + settings.SECRET_KEY).hexdigest() }
        super(CaptchaContactForm, self).__init__(initial=initial, *args, **kwargs)
        self.fields['captcha'].label = 'Type the word "%s" (to deter automated spam bots)' % captcha_value
    
    captcha = forms.CharField(widget=forms.TextInput(attrs=attrs_dict))
    hash = forms.CharField(max_length=40, widget=forms.HiddenInput())
    
    def clean_captcha(self):
        """
        If the value of the captcha field doesn't properly hash to the
        hidden pre-calculated value, raise a validation error.
        
        """
        if 'captcha' in self.cleaned_data and 'hash' in self.cleaned_data:
            if sha.new(self.cleaned_data['captcha'] + settings.SECRET_KEY).hexdigest() == self.cleaned_data['hash']:
                return self.cleaned_data['captcha']
            raise forms.ValidationError(u"You didn't type the word correctly")
