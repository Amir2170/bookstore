from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ValidationError
from django.contrib.auth.views import (
	PasswordResetView, 
	PasswordResetConfirmView,
)

from .forms import( 
	UserCreationForm, 
	AuthenticationForm, 
	CustomPasswordResetForm, 
	CustomPasswordResetConfirmForm,
)

def signup_view(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			form.clean_password2()
			email = form.cleaned_data.get('email')
			raw_password = form.clean_password2()
			user = authenticate(email=email, password=raw_password)
			login(request, user)
			return redirect(reverse('shop:home'))
	else:
		form = UserCreationForm()

	return render(request, 'accounts/signup.html', {"form": form})


def logout_view(request):
	logout(request)
	return redirect(reverse('shop:home'))


def login_view(request):
	if request.method == 'POST':
		form = AuthenticationForm(request.POST)
		if form.is_valid():
			form.clean()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password')
			user = authenticate(request, email=email, password=raw_password)
			login(request, user)
			return redirect(reverse('shop:home'))
	else:
		form = AuthenticationForm()

	return render(request, 'accounts/login.html', {"form": form})


class CustomPasswordResetView(PasswordResetView):
	form_class = CustomPasswordResetForm


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
	form_class = CustomPasswordResetConfirmForm