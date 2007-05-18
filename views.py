from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from contact_form.forms import ContactForm

def contact_form(request, form_class=ContactForm, template_name='contact/contact_form.html', success_url='/contact/sent/', login_required=False,):
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
    ``contact/contact_form.html``.

    To specify a URL to redirect to after a successfully-sent message,
    pass the ``success_url`` keyword argument; if not supplied, this
    will default to ``/contact/sent/``.
    
    To allow only registered users to use the form, pass a ``True``
    value for the ``login_required`` keyword argument.
    
    """
    if login_required and not request.user.is_authenticated():
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.path)

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid:
            if form.save():
                return HttpResponseRedirect(success_url)
    else:
        form = form_class()
    return render_to_response(template_name,
                              { 'form': form },
                              context_instance=RequestContext(request))
