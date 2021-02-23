from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser):
	email = models.EmailField(
			verbose_name='آدرس ایمیل',
			max_length=255,
			unique=True,
			)
	phone = PhoneNumberField(verbose_name='شماره تلفن')
	name = models.CharField(verbose_name='اسم', max_length=100)

	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	objects = CustomUserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name',]

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True

	@property
	def is_staff(self):
		return self.is_admin
