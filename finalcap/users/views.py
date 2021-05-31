from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, UserUpdateForm , ProfileUpdateForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Profile
from django.views.generic import ListView, DetailView

# Create your views here.
@login_required
def user_list(request):
	context = {
	'users':User.objects.all()
	}
	return render(request, 'users/user_list.html', context)

class PostListView(ListView):
	model = User
	template_name = 'users/user_list.html'
	context_object_name = 'users'
	ordering = ['-last_login']
	paginate_by = 100

class PostDetailView(DetailView):
	model = User
	template_name = 'users/user_detail.html'
	context_object_name = 'user'

@login_required
def profile(request):

	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your profile has been updated')
			return redirect('profile')

	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	context = {
	'u_form': u_form,
	'p_form': p_form
	}
	return render(request, 'users/profile.html', context)

def login(request):
	return render(request, 'users/login.html')

def logout(request):
	messages.success(request, f'You have been successfully signed out')
	return render(request, 'users/logout.html')

def password_reset(request):
	return render(request, 'users/password_reset.html')

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Your account has been created! You are now able to log in')
			return redirect('fileshare_dashboard')
	else:
		form = UserRegisterForm()

	return render(request, 'users/register.html', {'form':form})

