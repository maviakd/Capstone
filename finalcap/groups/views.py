from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View
from fileshare.models import Files
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.contrib.auth.models import User, ContentType, Permission
from .models import MyGroup
from fileshare.models import Files
from django.contrib import messages

class GroupLeaveView(View):
	def get(self, request, *args, **kwargs):
		group = MyGroup.objects.get(pk=kwargs.get('pk'))
		content = {"group":group}
		return render(request, "groups/group_leave.html", content)


	def post(self, request, *args, **kwargs):
		group = MyGroup.objects.get(pk=kwargs.get('pk'))
		group.user_set.remove(request.user) 
		messages.success(request, f'You have left Group (({group}))')
		return redirect("group_list")

class GroupView(View):
	def get(self, request, *args, **kwargs):
		group = MyGroup.objects.all()
		totgroups = 0
		owned_groups = []
		can_remove = [] #27
		can_view = [] #28
		part_of = []

		for item in group: # check groups
			if item.creator != request.user: # Group not created by you
				for user in item.user_set.all(): # Checking users in group
					if user == request.user: # If you in a group that you did not create
						if item.permissions.all(): # File has permissions
							for perm in item.permissions.all():
								if perm.id == 27:
									if not (item in part_of): # Duplication check
										can_remove.append(item) # Files you can delete
								elif perm.id == 28:
									if not (item in part_of): # Duplication check
										can_view.append(item) # Files you can view
						else: # Group has no permissions no permissions
							if not (item in part_of): # Duplication check
								part_of.append(item) # Files you can view
			else:
				owned_groups.append(item)
		for a1 in can_remove:
			part_of.append(a1)
		for a2 in can_view:
			part_of.append(a2)



		context = {'group':group, 'totgroups':totgroups, 'can_remove':can_remove, 'can_view':can_view, 'owned_groups':owned_groups, 'part_of':part_of}
		return render(request, 'groups/group_list.html', context)


	def post(self, request, *args, **kwargs):
		pass



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

class GroupRemoveView(View):
	def get(self, request, *args, **kwargs):
		group = MyGroup.objects.get(pk=kwargs.get('pk'))
		content = {'group':group}
		return render(request, "groups/group_remove_group.html", content)

	def post(self, request, *args, **kwargs):
		group = MyGroup.objects.get(pk=kwargs.get('pk'))
		MyGroup.delete(group)
		return redirect("group_list")


def group_list(request):
	group = MyGroup.objects.all()
	totgroups = 0

	for item in group:
		totgroups+=1

	context = {
	'group':group,
	'totgroups':totgroups
	}

	return render(request, 'groups/group_list.html', context)

class GroupRemoveFile(View):
	def get(self, request, *args, **kwargs):
		file = Files.objects.get(pk=kwargs.get('id'))
		group = MyGroup.objects.get(pk=kwargs.get('pk'))
		context = {'file':file, "group":group}
		return render(request, 'groups/group_remove_file.html', context)


	def post(self, request, *args, **kwargs):
		file = Files.objects.get(pk=kwargs.get('id'))
		group = MyGroup.objects.get(pk=kwargs.get('pk'))
		group.files_set.remove(file)
		return redirect("group_list")

class GroupAddFile(View):
	def get(self, request, *args, **kwargs):
		file = Files.objects.get(pk=kwargs.get('id'))
		group = MyGroup.objects.get(pk=kwargs.get('pk'))
		context = {'file':file, "group":group}
		messages.success(request, f'File {file} has been removed from {group}')
		return render(request, 'groups/group_add_file.html', context)

	def post(self, request, *args, **kwargs):
		file = Files.objects.get(pk=kwargs.get('id'))
		group = MyGroup.objects.get(pk=kwargs.get('pk'))
		group.files_set.add(file)
		messages.success(request, f'File {file} has been added to {group}')
		return redirect("group_list")



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
		return redirect(f"group_list")

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

		for things in perms:
			if things.id == 25:
				perms = perms.exclude(id = things.id)
			if things.id == 26:
				perms = perms.exclude(id = things.id)

		POG = perms


		UIG = group.user_set.all()
		users = User.objects.all()
		UOG = users
		FIG = group.files_set.all()
		all_files = Files.objects.all()
		FOG = []


		for item in all_files:
			if item.author == group.creator:
				FOG.append(item)

		if not(request.user in UIG):
			group.user_set.add(request.user)
			UIG = group.user_set.all()

		for item in FIG:
			for file in FOG:
				if item ==  file:
					FOG.remove(item)

		for item in PIG:
			for perm in perms:
				if item == perm:
					POG = POG.exclude(id = item.id)
		for item in UIG:
			for user in users:
				if item == user:
					UOG = UOG.exclude(username = user)




		context = {"UIG":UIG, "UOG":UOG, "PIG":PIG, "POG":POG, "group":group, 'FIG':FIG, 'FOG':FOG}
		return render(request, 'groups/group_update.html', context)

	def post(self, request, *args, **kwargs):

		user = User.objects.get(pk=kwargs.get('pk'))
		return redirect("fileshare-home")



