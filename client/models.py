from django.db import models
from django.db.models import Sum
# from asggotta.uuid_config import UUIDField
import uuid
from django.contrib.auth.models import User
from custom.models import *
from product.models import *

class Client(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, null=True, blank=True,verbose_name="Munisipiu",related_name="clientmun")
	administrativepost = models.ForeignKey(AdministrativePost, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Postu administrativu",related_name="clientpost")
	village = models.ForeignKey(Village, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Suku",related_name="clientvillage")
	firstname = models.CharField(max_length=200, null=True, verbose_name="Naran Propriu")
	lastname = models.CharField(max_length=200, null=True, verbose_name="Apelidu")
	pob = models.CharField(max_length=100, null=True, blank=True, verbose_name="Fatin Moris")
	dob = models.DateTimeField(null=True, blank=True, verbose_name="Data Moris")
	sex = models.CharField(choices=[('Mane','Mane'),('Feto','Feto')], max_length=10, null=True, verbose_name="Sexu")
	address = models.CharField(max_length=100, null=True, blank=True, verbose_name="Enderesu (Aldeia/Bairu)")
	phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Nu. Telemovel")
	is_active = models.BooleanField(default=True, null=True)
	image = models.ImageField(upload_to='Client', null=True,blank=True)
	datetime = models.DateTimeField(null=True)
	user_created = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)

	def __str__(self):
		template = '{0.firstname} {0.lastname}, {0.municipality} ({0.is_active})'
		return template.format(self)

class ClientUser(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name="clientuser")
	user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="clientuser")
	date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)

	def __str__(self):
		template = '{0.client.firstname} / {0.user} '
		return template.format(self)

class Pedidu(models.Model):
	kodigupedidu = models.CharField(max_length=100, null=True, blank=True, verbose_name="Kodigu Pedidu")
	client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="clientpedidu")
	datapedidu = models.DateField(null=True)
	datasimuprodutu = models.DateField(null=True,blank=True)
	is_sent = models.BooleanField(default=False, null=True)
	is_ontheway = models.BooleanField(default=False, null=True)
	is_delivered = models.BooleanField(default=False, null=True)
	is_recieved = models.BooleanField(default=False, null=True)
	hashed = models.CharField(max_length=32, null=True)

	def getPediduProdutu(self):
		return PediduProdutu.objects.filter(pedidu=self)

	def totalpresu(self):
		presutotal = PediduProdutu.objects.filter(pedidu=self).aggregate(Sum('totalpresu'))['totalpresu__sum']
		return presutotal

	def __str__(self):
		template = '{0.client.firstname} '
		return template.format(self)	

class PediduProdutu(models.Model):
	pedidu = models.ForeignKey(Pedidu, on_delete=models.CASCADE, related_name="pedidu")
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
	unit = models.ForeignKey(ProductUnit, on_delete=models.CASCADE, null=True)
	totalprodutu = models.IntegerField(blank=True, null=True,verbose_name="Total Pedidu")
	totalpresu = models.DecimalField(decimal_places=2,max_digits=10,verbose_name="Total Presu",null=True)
	is_checked = models.BooleanField(default=False, null=True)
	is_delivered = models.BooleanField(default=False, null=True)
	is_recieved = models.BooleanField(default=False, null=True)
	hashed = models.CharField(max_length=32, null=True)
	def __str__(self):
		template = '{0.pedidu.client.firstname} '
		return template.format(self)	