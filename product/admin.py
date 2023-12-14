from django.contrib import admin
from .models import Product,ProductUnit,ProductUnitStock,ProductTransaction
# Register your models here.

admin.site.register(Product)
admin.site.register(ProductUnit)
admin.site.register(ProductUnitStock)
admin.site.register(ProductTransaction)

