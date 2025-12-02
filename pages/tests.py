from django.test import TestCase
from django.urls import reverse, resolve
from django.core import mail
from django.utils import timezone

from .views import HomeView, ContactView
from .models import Contact


class HomePageTests(TestCase):

    def test_home_url_resolves(self):
        url = reverse("home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_uses_correct_template(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "pages/home.html")

    def test_home_view_class(self):
        view = resolve(reverse("home")).func.view_class
        self.assertEqual(view, HomeView)

    def test_home_page_content(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Home")  # Adjust as needed


class ContactPageTests(TestCase):

    def test_contact_url_resolves(self):
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)

    def test_contact_uses_correct_template(self):
        response = self.client.get(reverse("contact"))
        self.assertTemplateUsed(response, "pages/contact.html")

    def test_contact_view_class(self):
        view = resolve(reverse("contact")).func.view_class
        self.assertEqual(view, ContactView)

    def test_contact_form_in_context(self):
        response = self.client.get(reverse("contact"))
        self.assertIn("form", response.context)

    def test_contact_invalid_submission(self):
        response = self.client.post(reverse("contact"), {
            "name": "",
            "email": "",
            "subject": "",
            "message": "",
        })

        # Should re-render form, not redirect
        self.assertEqual(response.status_code, 200)

        form = response.context.get("form")
        self.assertIsNotNone(form)
        self.assertFalse(form.is_valid())

        # Verify required errors
        self.assertIn("This field is required.", form.errors.get("name", []))
        self.assertIn("This field is required.", form.errors.get("email", []))
        self.assertIn("This field is required.", form.errors.get("subject", []))
        self.assertIn("This field is required.", form.errors.get("message", []))

    def test_contact_valid_submission_creates_object_and_sends_email(self):
        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "subject": "Test Subject",
            "message": "Test message content",
        }
        response = self.client.post(reverse("contact"), data)

        # Redirect to success page
        self.assertRedirects(response, reverse("contact_success"))

        # Contact object created
        self.assertEqual(Contact.objects.count(), 1)
        contact = Contact.objects.first()
        self.assertEqual(contact.name, "John Doe")
        self.assertEqual(contact.email, "john@example.com")

        # Email sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Test Subject", mail.outbox[0].subject)
        self.assertIn("Test message content", mail.outbox[0].body)


class ContactSuccessPageTests(TestCase):

    def test_contact_success_page_renders(self):
        response = self.client.get(reverse("contact_success"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/contact_success.html")


class ContactModelTests(TestCase):

    def test_contact_model_creation(self):
        contact = Contact.objects.create(
            name="Alice",
            email="alice@example.com",
            subject="Hello",
            message="Testing model",
            created_at=timezone.now()
        )
        self.assertIsNotNone(contact.id)

    def test_required_fields(self):
        contact = Contact(
            name="",
            email="",
            subject="",
            message=""
        )

        with self.assertRaises(Exception):
            contact.full_clean()  # Trigger model validation

    def test_contact_str_representation(self):
        contact = Contact.objects.create(
            name="Bob",
            email="bob@example.com",
            subject="Subject",
            message="Message",
            created_at=timezone.now()
        )
        self.assertEqual(str(contact), "Bob - bob@example.com")