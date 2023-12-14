from django.contrib import admin
from client.models import Client,ClientUser,PediduProdutu,Pedidu
# Register your models here.

admin.site.register(Client)
admin.site.register(ClientUser)
admin.site.register(Pedidu)
admin.site.register(PediduProdutu)