from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.urls import reverse

from .forms import UserCreationForm


def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password')
			login(request, user)
			return redirect(reverse('shop:home'))
	else:
		form = UserCreationForm()

	return render(request, 'accounts/signup.html', {"form": form})