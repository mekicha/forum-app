from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.urls import resolve
from django.test import TestCase

from ..views import signup
from ..forms import SignupForm

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
		self.assertIsInstance(form, SignupForm)

	# def test_form_inputs(self):
	# 	self.assertContains(self.response,'<input', 5)
	# 	self.assertContains(self.response, 'type="text"', 1)
	# 	self.assertContains(self.response, 'type="email"', 1)
	# 	self.assertContains(self.response, 'type="password"', 2)


class SuccessfulSignUpTests(TestCase):
	def setUp(self):
		url = reverse('signup')
		data = {
			'username': 'johnson',
			'email': 'johnson@gmail.com',
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


class InvalidSignupTests(TestCase):
	def setUp(self):
		url = reverse('signup')
		self.response = self.client.post(url, {})

	def test_signup_status_code(self):
		self.assertEqual(self.response.status_code, 200)

	def test_form_errors(self):
		form = self.response.context.get('form')
		self.assertTrue(form.errors)

	def test_user_not_created(self):
		self.assertFalse(User.objects.exists())


