from django import forms
from django.contrib.auth.forms import( 
	ReadOnlyPasswordHashField, 
	PasswordResetForm,
	 SetPasswordForm,
	)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate

from .models import CustomUser


class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(
		label=_('Password'), widget=forms.PasswordInput
	)
	password2 = forms.CharField(
		label=_('Repeat Password'), widget=forms.PasswordInput
	)

	class Meta:
		model = CustomUser
		fields = ('email', 'phone', 'name',)

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise ValidationError(
				_('passwords do not match'),
				code='non match passwords'
			)
		return password2

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user


class UserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = CustomUser
		fields = ('email', 'phone', 'name', 
			'is_active', 'is_admin'
		)

	def clean_password(self):
		return self.initial['password']


class AuthenticationForm(forms.Form):

	email = forms.EmailField(label=_('Email'))
	password = forms.CharField(
		label=_('Password'),
		strip=False,
		widget=forms.PasswordInput(),
	)

	error_messages = {
		'invalid_login': _( 
			"password or email is incorrect note"
			" that both fields are case sensitive"
		),
		'inactive': _("specified account is inactive"),
	}

	def confirm_login_allowed(self, user):
		"""
			control whether the user can login or not
		"""
		if not user.is_active:
			raise ValidationError(
				self.error_messages['inactive'],
				code='inactive',
			)

	def get_invalid_login_error(self):
		return ValidationError(
			 self.error_messages['invalid_login'],
			code='invalid_login',
		)

	def clean(self):
		cleaned_data = super().clean()
		email = cleaned_data.get('email')
		password = cleaned_data.get('password')

		if email is not None and password:
			user_cache = authenticate(email=email, password=password)
			if user_cache is None:
				raise self.get_invalid_login_error()
			else:
				self.confirm_login_allowed(user_cache)

class CustomPasswordResetForm(PasswordResetForm):
	email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )


class CustomPasswordResetConfirmForm(SetPasswordForm):
	error_messages = {
		'password_mismatch': _('passwords do not match'),
   	}
	new_password1 = forms.CharField(
		label=_("New password"),
		strip=False,
		widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
	)
	new_password2 = forms.CharField(
		# Translators: This field is password repeat
		label=_("Repeat new password"),
		strip=False,
		widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
   	)




