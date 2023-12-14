from django.db import models
import uuid
from django.contrib.auth.models import User

class Product(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=200, null=True, verbose_name="Naran Produtu")
	volume = models.CharField(max_length=200, null=True, verbose_name="Volume")
	is_active = models.BooleanField(default=True, null=True)
	image = models.ImageField(upload_to='Product', null=True,blank=True)
	datetime = models.DateTimeField(null=True)
	user_created = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)

	def __str__(self):
		template = '{0.name} {0.volume} ({0.is_active})'
		return template.format(self)

class ProductUnit(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True,related_name="productunit")
	unit = models.CharField(max_length=200, null=True, verbose_name="Unidade")
	is_active = models.BooleanField(default=True, null=True)
	price = models.DecimalField(decimal_places=2,max_digits=10,verbose_name="Presu",null=True)
	datetime = models.DateTimeField(null=True)
	user_created = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)

	def unitStock(self):
		total = ProductUnitStock.objects.filter(unit=self).last()
		return total.total_update

	def __str__(self):
		template = '{0.product.name} | {0.unit}'
		return template.format(self)

class ProductUnitStock(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True,related_name="productstock")
	unit = models.ForeignKey(ProductUnit, on_delete=models.CASCADE, null=True,related_name="productstock")
	total = models.IntegerField(blank=True, null=True,verbose_name="Total Tama")
	total_update = models.IntegerField(blank=True, null=True,verbose_name="Total Update")
	total_update_pedidu = models.IntegerField(default=0,blank=True, null=True,verbose_name="Total Update bazeia ba Pedidu")
	total_out = models.IntegerField(blank=True, null=True,verbose_name="Total Sai")

	def __str__(self):
		template = '{0.product} {0.unit} {0.total}'
		return template.format(self)

class ProductTransaction(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
	unit = models.ForeignKey(ProductUnit, on_delete=models.CASCADE, null=True)
	date = models.DateField(null=True)
	total_in = models.IntegerField(blank=True, null=True,verbose_name="Total Tama")
	total_out = models.IntegerField(blank=True, null=True,verbose_name="Total Distribui")
	total = models.IntegerField(blank=True, null=True,verbose_name="Total")
	is_confirm = models.BooleanField(default=False, null=True)
	user_created = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
	hashed = models.CharField(max_length=32, null=True)

	def __str__(self):
		template = '{0.product} {0.unit} {0.total}'
		return template.format(self)


