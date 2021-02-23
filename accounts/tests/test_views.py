from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class TestSignupView(TestCase):

	def test_signup_view_uses_correct_template(self):
		response = self.client.get(reverse('accounts:signup'))
		self.assertTemplateUsed(response, 'accounts/signup.html')

	def test_signup_view_creates_a_user(self):
		response = self.client.post(reverse('accounts:signup'),	data={
			'email': 'testuser1@gmail.com',
			'phone': '+989133333333',
			'name': 'amir',
			'password1': 'testuser1',
			'password2': 'testuser2',
			}
		)
		user = User.objects.get(email='testuser1@gmail.com')
		