from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
#from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.

def login(request):
	return render(request, 'users/login.html')

def logout(request):
	return render(request, 'users/logout.html')

def profile(request):
	return render(request, 'users/profile.html')

def register(request):
#	form = UserCreationForm()
#	return render(request, 'users/register.html', {'form':form})
	return render(request, 'users/register.html')

def forgot_password(request):
	return render(request, 'users/forgot_password.html')

































