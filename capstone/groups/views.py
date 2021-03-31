from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View
from fileshare.models import Files
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.contrib.auth.models import User, Group, ContentType, Permission
from .models import MyGroup
from fileshare.models import Files
from django.contrib import messages

class GroupAddPermission(View):
	def get(self, request, *args, **kwargs):
		perm = Permission.objects.get(pk=kwargs.get('id'))
		group = MyGroup.objects.get(pk=kwargs.get('pk'))
		content = {'perm':perm, "group":group}
		return render(request, "groups/group_add_permission.html", content)


	def post(self, request, *args, **kwargs):
		perm = Permission.objects.get(pk=kwargs.get('id'))
		group = MyGroup.objects.get(pk=kwargs.get('pk'))
		group.permissions.add(perm.id)
		messages.success(request, f'Permission (({perm})) has been added to  (({group}))')
		return redirect("group_list")

class GroupRemovePermission(View):
	def get(self, request, *args, **kwargs):
		perm = Permission.objects.get(pk=kwargs.get('id'))
		group = MyGroup.objects.get(pk=kwargs.get('pk'))
		content = {'perm':perm, "group":group}
		return render(request, "groups/group_remove_permission.html", content)


	def post(self, request, *args, **kwargs):
		perm = Permission.objects.get(pk=kwargs.get('id'))
		group = MyGroup.objects.get(pk=kwargs.get('pk'))
		group.permissions.remove(perm.id)
		messages.success(request, f'Permission (({perm})) has been removed from (({group}))')
		return redirect("group_list")


class GroupCreateView(CreateView):
	model = MyGroup
	template_name = 'groups/group_create.html'
	context_object_name = 'group'

	fields = ['name']
	success_url = '/groups/'
	def form_valid(self, form):
		form.instance.creator = self.request.user
		return super().form_valid(form)

def group_list(request):
	context = {
	'group':Group.objects.all()
	}
	return render(request, 'groups/group_list.html', context)

class GroupAddUser(View):
	def get(self, request, *args, **kwargs):
		user = User.objects.get(pk=kwargs.get('id'))
		group = MyGroup.objects.get(pk=kwargs.get('pk'))
		context = {'user':user, "group":group}
		return render(request, 'groups/group_add_user.html', context)

	def post(self, request, *args, **kwargs):
		user = User.objects.get(pk=kwargs.get('id'))
		group = MyGroup.objects.get(pk=kwargs.get('pk'))
		group.user_set.add(user)
		messages.success(request, f'User {user} has been added to {group}')
		return redirect("group_list")

class GroupRemoveUser(View):
	def get(self, request, *args, **kwargs):
		user = User.objects.get(pk=kwargs.get('id'))
		group = MyGroup.objects.get(pk=kwargs.get('pk'))
		context = {'user':user, "group":group}
		return render(request, 'groups/group_remove_user.html', context)

	def post(self, request, *args, **kwargs):
		user = User.objects.get(pk=kwargs.get('id'))
		group = MyGroup.objects.get(pk=kwargs.get('pk'))
		group.user_set.remove(user)
		messages.success(request, f'User {user} has been removed from {group}')
		return redirect("group_list")

class GroupUpdateView(View):
	def get(self, request, *args, **kwargs):
		group = MyGroup.objects.get(pk=kwargs.get('pk'))
		PIG = group.permissions.all()
		content_type = ContentType.objects.get(app_label='fileshare', model = 'files')
		perms = Permission.objects.filter(content_type=content_type)
		POG = perms
		UIG = group.user_set.all()
		users = User.objects.all()
		UOG = users

		for item in PIG:
			for perm in perms:
				if item == perm:
					POG = POG.exclude(id = item.id)
		for item in UIG:
			for user in users:
				if item == user:
					UOG = UOG.exclude(username = user)


		context = {"UIG":UIG, "UOG":UOG, "PIG":PIG, "POG":POG, "group":group}
		return render(request, 'groups/group_update.html', context)

	def post(self, request, *args, **kwargs):

		user = User.objects.get(pk=kwargs.get('pk'))
		print("BBBBBBBBBBBBIIIIIIIIIIIIIIIIINNNNNNNNNNNNGGGGGGGGGGGGGG")
		return redirect("fileshare-home")



