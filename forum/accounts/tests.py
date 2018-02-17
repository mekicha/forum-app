from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.urls import resolve
from django.test import TestCase

from .views import signup

class SignupTests(TestCase):
	def setUp(self):
		url = reverse('signup')
		self.response = self.client.get(url)

	def test_signup_status_code(self):
		self.assertEqual(self.response.status_code, 200)

	def test_signup_url_resolves_view(self):
		view = resolve('/signup/')

		self.assertEqual(view.func, signup)

	def test_csrf(self):
		self.assertContains(self.response, 'csrfmiddlewaretoken')

	def test_contains_form(self):
		form = self.response.context.get('form')
		self.assertIsInstance(form, UserCreationForm)


class SuccessfulSignUpTests(TestCase):
	def setUp(self):
		url = reverse('signup')
		data = {
			'username': 'johnson',
			'password1': 'boardtest2020',
			'password2': 'boardtest2020'
		}
		self.response = self.client.post(url, data)
		self.home_url = reverse('home')

	def test_redirection(self):
		self.assertRedirects(self.response, self.home_url)

	def test_user_creation(self):
		self.assertTrue(User.objects.exists())

	def test_user_authentication(self):
		response = self.client.get(self.home_url)
		user = response.context.get('user')
		self.assertTrue(user.is_authenticated)