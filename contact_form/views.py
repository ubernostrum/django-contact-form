"""
View which can render and send email from a contact form.

"""


from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from contact_form.forms import ContactForm


def contact_form(request, form_class=ContactForm,
                 template_name='contact_form/contact_form.html',
                 success_url='/contact/sent/', fail_silently=False):
    """
    Renders a contact form, validates its input and sends an email
    from it.
    
    To specify the form class to use, pass the ``form_class`` keyword
    argument; if no ``form_class`` is specified, the base
    ``ContactForm`` class will be used.
    
    To specify the template to use for rendering the form (*not* the
    template used to render the email message sent from the form,
    which is handled by the form class), pass the ``template_name``
    keyword argument; if not supplied, this will default to
    ``contact_form/contact_form.html``.
    
    To specify a URL to redirect to after a successfully-sent message,
    pass the ``success_url`` keyword argument; if not supplied, this
    will default to ``/contact/sent/``.
    
    To suppress exceptions raised during sending of the email, pass a
    ``True`` value for the ``fail_silently`` keyword argument. This is
    **not** recommended.
    
    Template::
    
        Passed in the ``template_name`` argument.
        
    Context::
    
        form
            The form instance.
    
    """
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES, request=request)
        if form.is_valid():
            form.save(fail_silently=fail_silently)
            return HttpResponseRedirect(success_url)
    else:
        form = form_class(request=request)
    return render_to_response(template_name,
                              { 'form': form },
                              context_instance=RequestContext(request))
