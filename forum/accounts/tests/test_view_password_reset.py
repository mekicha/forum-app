from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm 
from django.core import mail 
from django.core.urlresolvers import reverse
from django.urls import resolve
from django.test import TestCase

class PasswordResetTests(TestCase):
	def setUp(self):
		url = reverse('password_reset')
		self.response = self.client.get(url)

	def test_status_code(self):
		self.assertEqual(self.response.status_code, 200)

	def test_view_function(self):
		view = resolve('/reset/')
		self.assertEqual(view.func, auth_views.PasswordResetView.as_view())

	def test_csrf(self):
		self.assertContains(response, 'csrfmiddlewaretoken')

	def test_contains_form(self):
		form = self.response.context.get('form')
		self.assertIsInstance(form, PasswordResetForm)

	def test_form_inputs(self):
		self.assertContains(self.response,'<input', 2)
		self.assertContains(self.response,'type="email"', 1)


class SuccessfulPasswordResetTests(TestCase):
    def setUp(self):
        email = 'john@doe.com'
        User.objects.create_user(username='john', email=email, password='123abcdef')
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': email})

    def test_redirection(self):
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)

    def test_send_password_reset_email(self):
        self.assertEqual(1, len(mail.outbox))

