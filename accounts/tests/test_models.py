from django.test import TestCase
from django.contrib.auth import get_user_model
from bookstore_project import settings

User = get_user_model()


class TestUserModel(TestCase):

	def test_custom_user_model_creation(self):
		user = User.objects.create_user(
			email='test@user.com',
			name='testuser',
			phone='09111111111',
			password='test123'
		)
		self.assertEqual(user.email, 'test@user.com')