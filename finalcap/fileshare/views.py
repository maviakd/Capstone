from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View
from .models import Files, Crypt, Thumb
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .forms import FileAuthForm1, FileAuthForm2, FileAuthForm3
from django.contrib import messages
from django.http import HttpResponse
from Crypto.Cipher import AES
from twilio.rest import Client
import hashlib, threading, time
from groups.models import MyGroup
import os

account_sid = ""
auth_token  = ""

class ResetView(View):
	def get(self, request, *args, **kwargs):

		return render(request, 'fileshare/file_reset.html')

	def post(self, request, *args, **kwargs):
		files = Files.objects.filter(author = request.user)
		groups = MyGroup.objects.filter(creator = request.user)
		fcount = 0
		gcount = 0

		for file in files:
			Files.delete(file)
			fcount += 1
		for group in groups:
			MyGroup.delete(group)
			gcount += 1
		request.user.profile.total_owned_files = 0
		request.user.profile.total_owned_groups = 0
		request.user.profile.total_uploaded_files = 0
		request.user.profile.total_download_files = 0
		request.user.profile.save()
		messages.info(request,f"A total of {fcount} files were deleted and {gcount} groups were deleted")
		return redirect('fileshare_dashboard')

class VPN(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		address = request.user.email
		file1 = 'UK.ovpn'
		file2 = 'Germany.ovpn'
		phones = 'https://play.google.com/store/apps/details?id=net.openvpn.openvpn'
		comp = "https://openvpn.net/client-connect-vpn-for-windows/"
		body1 = "{self.request.user} has requested to send the keys to the VPN to this email. "
		body2 = "If you would like to access the VPN on your smartphone click on this link| {phones} |"
		body3 = "If you would like to access the VPN on your computer click on this link| {comp} | "
		body4 = "Use these files to connect to your desired location"
		subject = "VPN"
		os.system(f"echo '{self.request.user} has requested to send the keys to the VPN to this email. If you would like to access the VPN on your smartphone click on this link| {phones} | If you would like to access the VPN on your computer click on this link| {comp} | Use these files to connect to your desired location' | mailx -s {subject} {address} -A {file1} -A {file2}")
		return redirect('fileshare_dashboard')


def has_num(number):
	if number == None:
		return False
	else:
		return True

def blank(request):
	return render(request, 'fileshare/tab.html')

def dashboard(request):
	if request.user.is_authenticated:
		files = Files.objects.filter(author=request.user)
		groups = MyGroup.objects.filter(creator=request.user)
		request.user.profile.total_groups = len(groups)
		request.user.profile.total_owned_files = len(files)
		space = 0
		for file in files:
			space += os.path.getsize(file.doc.path)
		request.user.profile.space = space 


		request.user.profile.save()

		number = has_num(request.user.profile.phone)
		if not number:
			messages.info(request, f'Please go to profile and update phone number field for text notifications and better security')

		if request.user.is_superuser:
			context = {'docs':Files.objects.all()}
		else:
			context = {'docs':Files.objects.all()}
		return render(request, 'fileshare/dashboard.html', context)

	return render(request, 'users/login.html')

def recrypt(file, data):
	time.sleep(4)
	with open(file, 'wb') as we:
		we.write(data)
	return

def read_file(file):
	print("WE MADE IT TO READ FILE")
	with open(file, 'rb') as e:
		return e.read()
def write_file(file, data):
	with open(file, 'wb') as df:
		df.write(data)
	return

def send_msg(receiver, message):
	account_sid = ""
	auth_token  = ""
	client = Client(account_sid, auth_token)
	msg = client.messages.create(
	from_ = "9292012004",
	to = f"+1{receiver}",
	body = message
)

class FileAuth(View, LoginRequiredMixin):
	def get(self, request, *args, **kwargs):
		Rlink1 = "fileshare_dashboard"
		auth = Files.objects.get(pk=kwargs.get('pk'))
		number = has_num(request.user.profile.phone)
		if not number:
			messages.info(request, f'Please go to profile and update phone number field for text notifications and better security')
		if auth.encryption == Files.OPT1:
			pform = FileAuthForm1()
		elif auth.encryption == Files.OPT2:
			pform = FileAuthForm2()
		elif auth.encryption == Files.OPT3:
			pform = FileAuthForm3()
		else:
			messages.success(request, f'This form is not encrypted')
			pform = FileAuthForm2()

		context = {'pform':pform}
		return render(request, 'fileshare/file_auth.html', context)

	def post(self, request, *args, **kwargs):
		Rlink1 = "fileshare_dashboard"
		mode = AES.MODE_CFB
		auth = Files.objects.get(pk=kwargs.get('pk'))
		number = has_num(request.user.profile.phone)
		if not number:
			messages.info(request, f'Please go to profile and update phone number field for text notifications and better security')
		if auth.encryption == Files.OPT1:
			if request.POST['pin'] == auth.pin and auth.author.ivk.iv == request.user.ivk.iv:
				messages.success(request, f'AUTHENTICATED. The file will lock itself after 4 SECONDS')
				request.user.profile.total_download_files += 1
				request.user.profile.save()
				if number:
					msg = f"User {request.user} has accessed file {str(auth.doc)[6:]} labeled {auth.title}"

				E_F = ""
				D_F = ""
				key = hashlib.sha256(auth.pin.encode("utf8")).digest()
				iv = auth.author.ivk.iv[:16].encode("utf8")
				cipher = AES.new(key, mode, iv)

				E_F = read_file(auth.doc.path)
				D_F = cipher.decrypt(E_F)
				write_file(auth.doc.path, D_F)

				RR = threading.Thread(target = recrypt, args = [auth.doc.path, E_F])
				RR.start()
				return render(request, 'fileshare/file_view.html', {'item':auth})

			else:
				messages.success(request, f'NOT AUTHENTICATED')
				if request.user != auth.creator:
					message.error(request, 'File encrypted using IVK which is unique for each account')
			return redirect(Rlink1)


		elif auth.encryption == Files.OPT2:
			if request.user.ivk.iv == auth.author.ivk.iv:
				messages.success(request, f'AUTHENTICATED. The file will lock itself after 4 SECONDS')
				request.user.profile.total_download_files += 1
				request.user.profile.save()
				if number:
					msg = f"User {request.user} has accessed file {str(auth.doc)[6:]} labeled {auth.title}"
					#send_msg(request.user.profile.phone, msg)

				key = hashlib.sha256(request.user.ivk.iv[:16].encode("utf8")).digest()
				cipher = AES.new(key, mode, auth.author.ivk.iv[:16].encode("utf8"))
				E_F = read_file(auth.doc.path)
				D_F = cipher.decrypt(E_F)
				write_file(auth.doc.path, D_F)
				RR = threading.Thread(target = recrypt, args = [auth.doc.path, E_F])
				RR.start()
				return render(request, 'fileshare/file_view.html', {'item':auth})

			else:
				messages.success(request, f'NOT AUTHENTICATED')
			return redirect(Rlink1)


		elif auth.encryption == Files.OPT3:
			if request.POST['pin'] == auth.pin:
				messages.success(request, f'AUTHENTICATED. The file will lock itself after 4 SECONDS')
				request.user.profile.total_download_files += 1
				request.user.profile.save()
				if number:
					msg = f"User {request.user} has accessed file {str(auth.doc)[6:]} labeled {auth.title}"
				key = hashlib.sha256(auth.pin.encode("utf8")).digest()
				cipher = AES.new(key, mode, Files.piv(auth).encode("utf8"))
				E_F = read_file(auth.doc.path)
				D_F = cipher.decrypt(E_F)
				write_file(auth.doc.path, D_F)
				RR = threading.Thread(target = recrypt, args = [auth.doc.path, E_F])
				RR.start()
				return render(request, 'fileshare/file_view.html', {'item':auth})

			else:
				messages.success(request, f'NOT AUTHENTICATED')
			return redirect(Rlink1)


		else:
			messages.success(request, f'NO AUTHENTICATION REQUIRED')
			request.user.profile.total_download_files += 1
			request.user.profile.save()
			if number:
				msg = f"User {request.user} has accessed file {str(auth.doc)[6:]} labeled {auth.title}"
			return render(request, 'fileshare/file_view.html', {'item':auth})

class PostListView(LoginRequiredMixin, View):
	paginate_by = 100
	def get(self, request, *args, **kwargs):
		files = Files.objects.all()
		owned_files = []
		owned_groups = []
		total_groups = 0
		part_of = []
		can_remove = [] #27
		can_view = [] #28
		group = MyGroup.objects.all()
		context = {}
		total_files = 0
		total_given_files = 0
		given_files = []


		for item in group: # check groups
			if item.creator != request.user: # Group not created by you
				for user in item.user_set.all(): # Checking users in group
					if user == request.user: # If you in a group that you did not create
						total_groups += 1
						if item.permissions.all(): # Group has permissions
							for perm in item.permissions.all(): # For every Permission
								if perm.id == 27: # if its delete
									for file in item.files_set.all(): # Checking files in that group with that permission
										if not (file in can_remove): # Duplication check
											can_remove.append(file) # Files you can delete
								elif perm.id == 28: # If its view
									for file in item.files_set.all(): # Checking files in that group with that permission
										if not (file in can_view): # Duplication check
											can_view.append(file) # Files you can view
						else: # Group has no permissions no permissions
							for file in item.files_set.all():
								if not (file in given_files): # Duplication check
									given_files.append(file) # Files you can view
			else:
				owned_groups.append(item)

		for i in can_remove:
			given_files.append(i)

		for i in can_view:
			given_files.append(i)

		for item in files:
			if item.author == request.user:
				owned_files.append(item)

		for c1 in owned_files:
			total_files +=1

		for c2 in given_files:
			total_given_files += 1

		for c3 in owned_groups:
			total_groups += 1


		request.user.profile.total_given_files = total_given_files
		request.user.profile.save()

		context = {'files':files, 'owned_files':owned_files, 'total_given_files':total_given_files, 'total_files':total_files, 'can_remove':can_remove, 'can_view':can_view, 'owned_groups':owned_groups, 'given_files':given_files}
		for item in files:

			if item.encryption == 'None':
				item.thumbnail = Thumb.thumb(item.doc)
			else:
				item.thumbnail = 'locked.jpg'

		return render(request, 'fileshare/file_home.html', context)

	def post(self, request, *args, **kwargs):
		pass


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Files
	template_name = 'fileshare/new_file.html'
	fields = ['title', 'doc', 'encryption', 'pin']
	success_url = '/files'

	def form_valid(self, form):
		form.instance.author = self.request.user
		self.request.user.profile.total_uploaded_files += 1
		self.request.user.profile.save()
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

class PostDeleteView(LoginRequiredMixin, DeleteView):
	model = Files
	template_name = 'fileshare/file_delete.html'
	success_url = '/files'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False
