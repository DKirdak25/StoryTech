from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.core.mail import send_mail
from django.conf import settings

from .form import ContactForm

class HomeView(TemplateView):
				template_name = "pages/home.html"
				
class ContactView(FormView):
    template_name = "pages/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact_success")

    def form_valid(self, form):
        # Save form data to the database
        contact = form.save()

        # Send email notification
        send_mail(
            subject=f"New Contact Message: {contact.subject}",
            message=f"Name: {contact.name}\nEmail: {contact.email}\n\nMessage:\n{contact.message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["dipalikirdak9@gmail.com"],  # Replace with your email
            fail_silently=False,
        )

        return super().form_valid(form)
        
class ContactSuccessView(TemplateView):
    template_name = "pages/contact_success.html"        
        
