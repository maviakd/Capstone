from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Files
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.contrib.auth.models import User, Group

# Create your views here.

def home(request):
	return render(request, 'fileshare/base.html')

def dashboard(request):
	if request.user.is_superuser:
		context = {'docs':Files.objects.all()}
	else:
		context = {'docs':Files.objects.filter(author=request.user)}
#	print(f"-------------------------------------------------------------------------------------------------------------{Files.objects.filter(author=request.user)}")
	return render(request, 'fileshare/dashboard.html', context)


class PostListView(LoginRequiredMixin, ListView):
	paginate_by = 3
	model = Files
	template_name= 'fileshare/home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Files
	template_name = 'fileshare/new_file.html'
	fields = ['title', 'doc']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Files
	fields = ['title', 'doc']
	template_name = 'fileshare/file_update.html'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Files
	template_name = 'fileshare/file_delete.html'
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


#def dashboard(request):
#	context = {'docs':Files.objects.all()}
#	return render(request, 'fileshare/dashboard.html', context)
