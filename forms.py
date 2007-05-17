"""
Base contact form and useful example functionality.

"""

import sha
from django import newforms as forms
from django.conf import settings
from django.template import Context, loader
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
    
    To add functionality, subclass this form; most of the heavy
    lifting happens in the ``get_message`` method, which must exist on
    all subclasses and which must return a dictionary with the
    following keys:

        * ``subject``: A string to use as the subject of the message.
        
        * ``recipient_list``: A list of email addresses to which
          the message should be sent.
          
        * ``message``: A string to use as the message body.

    If all you want to add in your subclass is extra validation,
    leaving the base ``get_message`` alone will work, and will return
    the following:

        * ``subject``: The name of the current ``Site`` in square
          brackets, followed by "Message sent through the web site".

        * ``recipient_list``: The email addresses specified in the
          ``MANAGERS`` setting.

        * ``message``: The output of rendering the template
          ``contact/base_contact_form.txt`` with the values of the
          ``name``, ``email`` and ``message`` fields.

    If a subclass defines ``__init__``, it must call this form's
    ``__init__`` via ``super``, and it must accept ``*args`` and
    ``**kwargs`` and pass them in the ``super`` call.
    
    Beyond that, the sky's the limit; anything which is supported by
    Django's newforms can be added in a subclass.
    
    """
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
    
    name = forms.CharField(max_length=100,
                           widget=forms.TextInput(attrs=attrs_dict),
                           label=u'Your name')
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=200)),
                             label=u'Your email address')
    message = forms.CharField(widget=forms.Textarea(attrs=attrs_dict),
                              label=u'Your message')
    
    def get_message(self):
        """
        Renders the message, using template
        ``contact/base_contact_form.txt``.
        
        """
        if not self.is_valid():
            raise ValueError("Message cannot be rendered from invalid contact form")
        t = loader.get_template('base_contact_form.txt')
        c = Context({ 'name': self.cleaned_data['name'],
                      'email': self.cleaned_data['email'],
                      'message': self.cleaned_data['message'] })
        return { 'subject': "[%s] Message sent through the web site" % Site.objects.get_current().name,
                 'recipient_list': [mail_tuple[1] for mail_tuple in settings.MANAGERS],
                 'message': t.render(c) }

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
    not supplied is 'swordfish', but you really should pass in
    something else. Choosing a random word from a dictionary file is a
    good method.
    
    """
    def __init__(self, captcha_value="swordfish", *args, **kwargs):
        super(CaptchaContactForm, self).__init__(*args, **kwargs)
        self.fields['setec_astronomy'] = sha.new(captcha_value + settings.SECRET_KEY).hexdigest()
        self.fields['captcha'].label = 'Type the word "%s" (to deter automated spam bots)' % captcha_value
        
    captcha = forms.CharField(widget=forms.TextInput(attrs=attrs_dict))
    setec_astronomy = forms.CharField(max_length=40, widget=forms.HiddenInput())
    
    def clean_captcha(self):
        """
        If the value of the captcha field doesn't properly hash to the
        hidden pre-calculated value, raise a validation error.
        
        """
        if 'captcha' in self.cleaned_data and 'setec_astronomy' in self.cleaned_data:
            if sha.new(self.cleaned_data['captcha'] + settings.SECRET_KEY).hexdigest() == self.cleaned_data['setec_astronomy']:
                return self.cleaned_data['captcha']
            raise forms.ValidationError(u"You didn't type the word correctly")


class AkismetContactForm(ContactForm):
    """
    Contact form which doesn't add any extra fields, but does add an
    Akismet spam check to the validation routine.
    
    Requires the setting ``AKISMET_API_KEY``, which should be a valid
    Akismet API key.
    
    When instantiating, pass the ``HttpRequest`` object as the keyword
    argument ``request``; this is necessary for Akismet to collect
    data for the spam check.
    
    """
    def __init__(self, request=None, *args, **kwargs):
        if request is None:
            raise ValueError("AkismetContactForm requires a 'request' keyword argument")
        super(AkismetContactForm, self).__init__(*args, **kwargs)
        self.request = request
    
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
