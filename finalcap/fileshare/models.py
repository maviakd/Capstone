from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from twilio.rest import Client
import hashlib, random, string
from Crypto.Cipher import AES
from twilio.rest import Client
from groups.models import MyGroup

# Create your models here.

class Crypt:

	def __init__(self, cipher):
		self.cipher = cipher

	def pad_file(self, file):
		self.file = file[0:len(file)-1]
		while len(self.file)% 16 != 0:
			self.file = self.file + b'0'
		return self.file

	def read_pad_enc_file(self, file):
		self.file = file
		with open(self.file, 'rb') as f:
			UIfile = f.read()
		return self.cipher.encrypt(Crypt(self.cipher).pad_file(UIfile))

	def write_enc(self, file, output_file):
		self.file = file
		self.output_file = output_file
		with open (self.output_file, 'wb') as e:
			e.write(self.file)

	def encrypt(self, file, output_file, write):
		self.file = file
		self.output_file = output_file
		self.write = write
		encrypted_file = Crypt(self.cipher).read_pad_enc_file(self.file)
		if self.write:
			Crypt(self.cipher).write_enc(encrypted_file, self.output_file)
		return encrypted_file

def send_msg(receiver, message):
	account_sid = ""
	auth_token  = ""
	client = Client(account_sid, auth_token)
	msg = client.messages.create(
	from_ = "9292012004",
	to = f"+1{receiver}",
	body = message
)

class Thumb:
	def thumb(file):
		file = str(file)
		images = ['jpg', 'jpeg', 'png']
		msw = ['doc', 'docx', 'dox']
		pdf = ['pdf']
		excel = ['xlsx']
		imgs = ['word.jpg', 'pdf.jpg', 'excel.jpg', 'file.jpg']

		for item in images:
			if item in file:
				return file
		for item in msw:
			if item in file:
				return imgs[0]
		for item in pdf:
			if item in file:
				return imgs[1]
		for item in excel:
			if item in file:
				return imgs[2]
		return imgs[3]



class Files(models.Model):
	title = models.CharField(max_length = 100)
	doc = models.FileField(upload_to='files')
	date_posted = models.DateTimeField(default = timezone.now)
	author = models.ForeignKey(User, on_delete = models.CASCADE)
	pin = models.CharField(max_length = 20, null = True, blank = True)
	thumbnail = models.ImageField(default="default.jpg")
	belongsto = models.ManyToManyField(MyGroup)

	OPT1 = "IVK & Pin"
	OPT2 = "IVK Only"
	OPT3 = "Pin Only"
	OPT4 = "None"

	encryption_methods = [(OPT1, "IVK & PIN"), (OPT2, 'IVK Only'), (OPT3, 'Pin Only'), (OPT4, "None")]
	encryption = models.CharField(choices = encryption_methods, default = 1, max_length = 20)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('user_detail', kwargs={'pk':self.author.pk})

	def piv(self):
		if len(str(self.pin)) < 16:
			missing = 16 - len(self.pin)
			return self.pin + self.author.ivk.iv[:missing]

	def save(self, *args, **kwargs):

		mode = AES.MODE_CFB

		if self.encryption == self.OPT1:
			key = hashlib.sha256(self.pin.encode("utf8")).digest()
			cipher = AES.new(key, mode, self.author.ivk.iv[:16].encode("utf8"))
			msg = f"Dear user {self.author}. Your file {self.doc} labeled {self.title} has been created with encryption method {self.encryption} with |PIN={self.pin}|. Only those with YOUR ACCOUNT AND FILE PIN will be able to access this filE"
		elif self.encryption == self.OPT2:
			key = hashlib.sha256(self.author.ivk.iv[:16].encode("utf8")).digest()
			cipher = AES.new(key, mode, self.author.ivk.iv[:16].encode("utf8"))
			msg = f"Dear user {self.author}. Your file {self.doc} labeled {self.title} has been created with encryption method {self.encryption}. Only those with YOUR ACCOUNT will be able to access this file"
		elif self.encryption == self.OPT3:
			key = hashlib.sha256(self.pin.encode("utf8")).digest()
			cipher = AES.new(key, mode, Files.piv(self).encode("utf8"))
			msg = f"Dear user {self.author}. Your file {self.doc} labeled {self.title} has been created with encryption method {self.encryption} with |PIN={self.pin}|. Only those with THE FILE PIN will be able to access this file"
		else:
			self.pin = None
			msg = f"Dear user {self.author}. Your file {self.doc} labeled {self.title} has been created WITHOUT an encryption method. EVERYONE will be able to access this file"

		SEND = False
		if SEND:
			send_msg(self.author.profile.phone, msg)

		super().save(Files, *args, **kwargs)

		if self.encryption != self.OPT4:
			mode = AES.MODE_CBC
			file = Crypt(cipher).encrypt(self.doc.path, self.doc.path, False)
			with open(self.doc.path, 'wb') as f:
				f.write(file)
