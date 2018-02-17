from django.core.urlresolvers import reverse
from django.urls import resolve
from django.test import TestCase

from .views import signup

class SignupTests(TestCase):
	def test_signup_status_code(self):
		url = reverse('signup')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)

	def test_signup_url_resolves_view(self):
		view = resolve('/signup/')

		self.assertEqual(view.func, signup)
