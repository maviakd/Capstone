from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View
from .models import Files, Crypt
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.contrib.auth.models import User, Group
from .forms import FileAuthForm1, FileAuthForm2, FileAuthForm3
from django.contrib import messages
from django.http import HttpResponse
from Crypto.Cipher import AES
from twilio.rest import Client
import hashlib, threading, time

account_sid = ""
auth_token  = ""

# Create your views here.

def has_num(number):
	if number == None:
		return False
	else:
		return True

def home(request):
	return render(request, 'fileshare/base.html')

def dashboard(request):
	number = has_num(request.user.profile.phone)
	messages.success(request, f'After Decryption File Will Lock In 4 Seconds')
	if not number:
		messages.info(request, f'Please go to Profile and update Phone Number Field for text notifications and better security')

	if request.user.is_superuser:
		context = {'docs':Files.objects.all()}
	else:
		context = {'docs':Files.objects.all()}
	return render(request, 'fileshare/dashboard.html', context)

def recrypt(file, data):
	time.sleep(4)
	with open(file, 'wb') as we:
		we.write(data)
	return

def read_file(file):
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

class FileAuth(View):
	def get(self, request, *args, **kwargs):
		Rlink1 = "fileshare-home"
		auth = Files.objects.get(pk=kwargs.get('pk'))
		print(f"----------------{auth.encryption}------------------------")
		number = has_num(request.user.profile.phone)
		messages.success(request, f'After Decryption File Will Lock In 4 Seconds')
		if not number:
			messages.info(request, f'Please go to Profile and update Phone Number Field for text notifications and better security')
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
		Rlink1 = "fileshare-home"
		mode = AES.MODE_CFB
		auth = Files.objects.get(pk=kwargs.get('pk'))
		number = has_num(request.user.profile.phone)
		if not number:
			messages.info(request, f'Please go to Profile and update Phone Number Field for text notifications and better security')
		if auth.encryption == Files.OPT1:
			if request.POST['pin'] == auth.pin and auth.author.ivk.iv == request.user.ivk.iv:
				messages.success(request, f'AUTHENTICATED')
				if number:
					msg = f"User {request.user} has accessed file {str(auth.doc)[6:]} labeled {auth.title}"
					send_msg(request.user.profile.phone, msg)

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
				print("------------------------------THE FILE HAS BEEN REINCRIPTED------------------------")
				return render(request, 'fileshare/file_view.html', {'item':auth})

			else:
				messages.success(request, f'NOT AUTHENTICATED')
			return redirect(Rlink1)


		elif auth.encryption == Files.OPT2:
			if request.user.ivk.iv == auth.author.ivk.iv:
				messages.success(request, f'AUTHENTICATED')
				if number:
					msg = f"User {request.user} has accessed file {str(auth.doc)[6:]} labeled {auth.title}"
					send_msg(request.user.profile.phone, msg)

				key = hashlib.sha256(request.user.ivk.iv[:16].encode("utf8")).digest()
				cipher = AES.new(key, mode, auth.author.ivk.iv[:16].encode("utf8"))
				E_F = read_file(auth.doc.path)
				D_F = cipher.decrypt(E_F)
				write_file(auth.doc.path, D_F)
				RR = threading.Thread(target = recrypt, args = [auth.doc.path, E_F])
				RR.start()
				print("------------------------------THE FILE HAS BEEN REINCRIPTED------------------------")
				return render(request, 'fileshare/file_view.html', {'item':auth})

			else:
				messages.success(request, f'NOT AUTHENTICATED')
			return redirect(Rlink1)


		elif auth.encryption == Files.OPT3:
			if request.POST['pin'] == auth.pin:
				messages.success(request, f'AUTHENTICATED')
				if number:
					msg = f"User {request.user} has accessed file {str(auth.doc)[6:]} labeled {auth.title}"
					send_msg(request.user.profile.phone, msg)
				key = hashlib.sha256(auth.pin.encode("utf8")).digest()
				cipher = AES.new(key, mode, Files.piv(auth).encode("utf8"))
				E_F = read_file(auth.doc.path)
				D_F = cipher.decrypt(E_F)
				write_file(auth.doc.path, D_F)
				RR = threading.Thread(target = recrypt, args = [auth.doc.path, E_F])
				RR.start()
				print("------------------------------THE FILE HAS BEEN REINCRIPTED------------------------")
				return render(request, 'fileshare/file_view.html', {'item':auth})

			else:
				messages.success(request, f'NOT AUTHENTICATED')
			return redirect(Rlink1)


		else:
			messages.success(request, f'NO AUTHENTICATION REQUIRED')
			if number:
				msg = f"User {request.user} has accessed file {str(auth.doc)[6:]} labeled {auth.title}"
				send_msg(request.user.profile.phone, msg)
			return render(request, 'fileshare/file_view.html', {'item':auth})

class PostListView(LoginRequiredMixin, ListView):
	paginate_by = 3
	model = Files
	template_name= 'fileshare/home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Files
	template_name = 'fileshare/new_file.html'
	fields = ['title', 'doc', 'encryption', 'pin']

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
