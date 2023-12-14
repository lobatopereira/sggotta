from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,Group
from custom.utils import *
from product.models import Product,ProductUnitStock
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users

# from ipware import get_client_ip
# from ip2geotools.databases.noncommercial import DbIpCity

# Create your views here.

@login_required
def home(request):
	products = ProductUnitStock.objects.all()
	context = {
		"title":"Sistema Jestaun Produsaun GOTTA",
		"products":products,
	}

	return render (request, 'index/indexAdmin.html',context)