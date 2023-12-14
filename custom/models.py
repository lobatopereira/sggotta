from django.db import models
# from asggotta.uuid_config import UUIDField
import uuid
# Create your models here.

class Municipality(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	code = models.CharField(max_length=5, null=True, blank = True)
	name = models.CharField(max_length=100)
	hckey = models.CharField(max_length=32, null=True ,  blank = True)
	date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class AdministrativePost(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=100)
	date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class Village(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	administrativepost = models.ForeignKey(AdministrativePost, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=100)
	date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class Aldeia(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	village = models.ForeignKey(Village, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=100)
	date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class AcademicLevel(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=50, verbose_name="Naran")
	date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class Religion(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length = 50,verbose_name='Relijiun')
	def __str__(self):
		template = '{0.name}'
		return template.format(self)
	class Meta:
		verbose_name_plural='Dadus Custom Ba Relijiaun'

class Profession(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length = 50 ,verbose_name='Profisaun Servisu')
	date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	def __str__(self):
		template = '{0.name}'
		return template.format(self)
	class Meta:
		verbose_name_plural='Dadus Custom Ba Profisaun'