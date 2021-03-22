from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from fileshare.models import Files
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.contrib.auth.models import User, Group
from .models import MyGroup
from .forms import GroupUserAdd
from fileshare.models import Files

class GroupCreateView(CreateView):
	model = MyGroup
	template_name = 'groups/group_create.html'
	context_object_name = 'group'

	fields = '__all__'
	success_url = '/groups/'
	def form_valid(self, form):
		form.instance.creator = self.request.user
		return super().form_valid(form)


class GroupDetailView(ListView):
	model = MyGroup
	template_name = 'groups/group_detail.html'
	context_object_name = 'group'
	fields = '__all__'


def group_list(request):
	context = {
	'group':Group.objects.all()
	}
	#users = User.objects.all()
	return render(request, 'groups/group_list.html', context)

class GroupUpdateView(UpdateView):
	model = MyGroup
	queryset = MyGroup.objects.all()
	template_name = 'groups/group_update.html'
	context_object_name = 'form'
	fields = '__all__'
	success_url = '/groups/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False



def group_update(request):
	if request.method == 'POST':
		form = GroupUserAdd(request.POST, instance=request.user)
#		print(f'--------------------------{request.method}-------------------------------{request.GET["item"]}')
	else:
		form = GroupUserAdd(instance=request.user)
#		print(f'--------------------------{request.method}-------------------------------{request.GET["item"]}')

	return render(request, 'groups/group_update.html', {'fiorm':form})


