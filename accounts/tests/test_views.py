from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib import auth
from django.core.exceptions import ValidationError

User = get_user_model()


class TestSignupView(TestCase):

	def setUp(self):
		self.response = self.client.post(reverse('accounts:signup'),	data={
			'email': 'testuser1@gmail.com',
			'phone': '+989133333333',
			'name': 'amir',
			'password1': 'testuser1',
			'password2': 'testuser1',
			}
		)

	def test_signup_view_uses_correct_template(self):
		response = self.client.get(reverse('accounts:signup'))
		self.assertTemplateUsed(response, 'accounts/signup.html')

	def test_signup_view_creates_a_user(self):
		user = User.objects.get(email='testuser1@gmail.com')
		self.assertRedirects(self.response, reverse('shop:home'))
		self.assertEqual(user.phone, '+989133333333')
		self.assertEqual(user.name, 'amir')

	def test_signedup_user_is_authenticated(self):
		user = User.objects.get(email='testuser1@gmail.com')
		self.assertIn('_auth_user_id', self.client.session)

	def test_signup_view_raises_validation_error_if_user_enters_two_different_passwords(self):
		response = self.client.post(reverse('accounts:signup'),	data={
			'email': 'testuser2@gmail.com',
			'phone': '+989133333333',
			'name': 'amir',
			'password1': 'testuser1',
			'password2': 'testuser2',
			}
		)
		self.assertIn('پسورد ها با هم مطابقت ندارند', 
			response.content.decode()
		)


class TestLogoutView(TestCase):

	def setUp(self):
		self.response = self.client.post(reverse('accounts:signup'),	data={
			'email': 'testuser1@gmail.com',
			'phone': '+989133333333',
			'name': 'amir',
			'password1': 'testuser1',
			'password2': 'testuser2',
			}
		)

	def test_logout_view_logsout_correctly(self):
		response = self.client.get(reverse('accounts:logout'))
		self.assertNotIn('_auth_user_id', self.client.session)

	def test_logout_view_redirect_to_the_main_page(self):
		response = self.client.get(reverse('accounts:logout'))
		self.assertRedirects(response, reverse('shop:home'))


class TestLoginVIew(TestCase):

	def setUp(self):
		User.objects.create_user(email='testuser1@gmail.com',
			phone='+989211333333',
			name='amir',
			password='testuser1',
		)
		self.error_messages = {
		'invalid_login': ( 
			"رمز عبور یا ایمیل اشتباه است دقت"
			" کنید که هر دو فیلد حساس به حروف بزرگ و کوچک است"
		),
		'inactive': ("اکانت کاربری مورد نظر غیر فعال است"),
	}

	def test_login_view_logs_an_existing_user_in(self):
		response = self.client.post(reverse('accounts:login'), data={
			'email': 'testuser1@gmail.com',
			'password': 'testuser1',
			}
		)
		self.assertIn('_auth_user_id', self.client.session)

	def test_login_view_redirects_to_home_page_after_logging_user_in(self):
		response = self.client.post(reverse('accounts:login'), data={
			'email': 'testuser1@gmail.com',
			'password': 'testuser1',
			}
		)
		self.assertRedirects(response, reverse('shop:home'))

	def test_login_view_raises_validation_error_if_credentials_are_wrong(self):
		response = self.client.post(reverse('accounts:login'), data={
			'email': 'testuser1@gmail.com',
			'password': 'testuser2',
			}
		)
		self.assertIn(self.error_messages['invalid_login'], 
			response.content.decode()
		)


class CustomPasswordResetView(TestCase):

	def setUp(self):
		User.objects.create_user(email='testuser1@gmail.com',
			phone='+989211333333',
			name='amir',
			password='testuser1',
		)

	def test_password_reset_page_loads_up_successfully(self):
		response = self.client.get(reverse('password_reset'))
		self.assertEqual(response.status_code, 200)

	def test_password_reset_view_sends_email_successfully(self):
		response = self.client.post(reverse('password_reset'), data={
			'email': 'testuser1@gmail.com',
			})
		self.assertRedirects(response, reverse('password_reset_done'))

	def test_password_reset_form_shows_correct_field_tag(self):
		response = self.client.get(reverse('password_reset'))
		self.assertIn('آدرس ایمی', response.content.decode())


	class CustomPasswordResetConfirmView(TestCase):
		def setUp(self):
			User.objects.create_user(email='testuser1@gmail.com',
				phone='+989211333333',
				name='amir',
				password='testuser1',
			)

		def test_password_change_page_loads_up_correctly(self):
			response = self.client.get(reverse('password_reset_confirm'))
			self.assertEqual(response.status_code, 200)