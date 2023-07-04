"""
View which can render and send email from a contact form.

"""

from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import ContactForm


class ContactFormView(FormView):
    """
    Base contact form view.

    """

    form_class = ContactForm
    recipient_list = None
    success_url = reverse_lazy("django_contact_form_sent")
    template_name = "django_contact_form/contact_form.html"

    def form_valid(self, form):
        """
        Handle a valid form by sending the email.

        """
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        """
        Override of base method in order to pass the HTTP request as a form keyword
        argument, and also the optional recipient_list (if set).

        """
        # ContactForm instances require instantiation with an
        # HttpRequest.
        kwargs = super().get_form_kwargs()
        kwargs.update({"request": self.request})

        # We may also have been given a recipient list when
        # instantiated.
        if self.recipient_list is not None:
            kwargs.update({"recipient_list": self.recipient_list})
        return kwargs
