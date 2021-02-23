from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import CustomUser


class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(
		label='رمز عبور', widget=forms.PasswordInput
	)
	password2 = forms.CharField(
		label='تکرار رمز عبور', widget=forms.PasswordInput
	)

	class Meta:
		model = CustomUser
		fields = ('email', 'phone', 'name',)

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			return ValueError('پسورد ها با هم مطابقت ندارند')
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















