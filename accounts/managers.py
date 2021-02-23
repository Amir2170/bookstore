from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):

	def create_user(self, email, phone, name, password=None):
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(
			email=self.normalize_email(email),
			phone=phone,
			name=name,
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, name, password=None):
		user = self.model(
			email=self.normalize_email(email),
			name=name,
		)
		user.is_admin=True
		user.set_password(password)
		user.save(using=self._db)
		return user