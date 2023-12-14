from django.db import models
# from asggotta.uuid_config import UUIDField
import uuid
from django.contrib.auth.models import User
from product.models import *
from client.models import *

# Create your models here.

class ProductSell(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True,blank=True)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
	unit = models.ForeignKey(ProductUnit, on_delete=models.CASCADE, null=True)
	date = models.DateField(null=True)
	total_out = models.IntegerField(blank=True, null=True,verbose_name="Total Distribui")
	totalprice = models.DecimalField(decimal_places=2,max_digits=10,blank=True, null=True,verbose_name="Total Presu")
	user_created = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	date_created = models.DateTimeField(auto_now_add=True,null=True,blank=True)

	def __str__(self):
		template = '{0.product.name} {0.unit} {0.total_out}'
		return template.format(self)
