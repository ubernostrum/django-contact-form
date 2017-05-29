from ..forms import AkismetContactForm
from ..views import ContactFormView


class AkismetView(ContactFormView):
    form_class = AkismetContactForm
