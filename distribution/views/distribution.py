from django.shortcuts import render,redirect, get_object_or_404,HttpResponse
from django.http import HttpResponse
from django.contrib.auth.models import User,Group
from custom.utils import *
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from client.models import *
from distribution.models import *
from distribution.forms import *
from users.models import Profile
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
# from ipware import get_client_ip
# from ip2geotools.databases.noncommercial import DbIpCity
import datetime
from django.contrib import messages
from django.db import transaction

@login_required
@allowed_users(allowed_roles=['admin','distribuicao'])
def DistDash(request):
	group = request.user.groups.all()[0].name
	objects = ProductUnitStock.objects.all()
	context = {
		"group":group,
		"title":"Painel Distribution Produtu GOTTA",
		"page":"dash",
		"objects":objects,
	}

	return render (request, 'distribution/dash.html',context)

@login_required
@allowed_users(allowed_roles=['admin','distribuicao'])
def DistOutAdd(request):
	group = request.user.groups.all()[0].name
	if request.method == 'POST':
		form = ProductSellForm(request.POST, request.FILES)
		if form.is_valid():
			with transaction.atomic():
				instance = form.save(commit=False)
				instance.user_created = request.user
				productunit = ProductUnit.objects.get(id=instance.unit.id)
				product = Product.objects.get(id=productunit.product.id)
				instance.unit = productunit
				instance.product = product
				totalSai = instance.total_out
				instance.total_in = 0
				lastTransantion = ProductTransaction.objects.filter(unit=productunit).order_by('id').last()
				if lastTransantion:
					instance.total = lastTransantion.total - totalSai
				else:
					messages.warning(request, f'Dadus Produsaun {product.name} GOTA Seidauk iha.')
					return redirect('distribution-dash')
				newTotal = instance.total
				instance.save()
				ProductTransaction.objects.create(date=instance.date,total_in=0,total_out=instance.total_out,total=newTotal,user_created=request.user,unit=productunit,product=product)
				productUnitStock = get_object_or_404(ProductUnitStock,unit=productunit,product=product)
				productUnitStock.total_update -= totalSai
				productUnitStock.total_out += totalSai
				productUnitStock.save()
				messages.success(request, f'Dadus Distribuisaun {product.name} GOTA rejista ona.')
				return redirect('distribution-dash')
	else:
		form = ProductSellForm()

	context = {
		"group":group,
		"title":"Rejista Distribuisaun Produtu GOTTA",
		"page":"form",
		"form":form,
	}

	return render (request, 'distribution/dash.html',context)

@login_required
@allowed_users(allowed_roles=['admin','distribuicao'])
def ProductDistOutAdd(request,id):
	group = request.user.groups.all()[0].name
	productunit = ProductUnit.objects.get(id=id)
	if request.method == 'POST':
		form = ProductSellForm1(request.POST, request.FILES)
		if form.is_valid():
			with transaction.atomic():
				instance = form.save(commit=False)
				instance.user_created = request.user
				# productunit = ProductUnit.objects.get(id=instance.unit.id)
				product = Product.objects.get(id=productunit.product.id)
				instance.unit = productunit
				instance.product = product
				totalSai = instance.total_out
				instance.total_in = 0
				lastTransantion = ProductTransaction.objects.filter(unit=productunit).order_by('id').last()
				if lastTransantion:
					instance.total = lastTransantion.total - totalSai
				else:
					messages.warning(request, f'Dadus Produsaun {product.name} GOTA Seidauk iha.')
					return redirect('distribution-dash')
				newTotal = instance.total
				instance.save()
				ProductTransaction.objects.create(date=instance.date,total_in=0,total_out=instance.total_out,total=newTotal,user_created=request.user,unit=productunit,product=product)
				productUnitStock = get_object_or_404(ProductUnitStock,unit=productunit,product=product)
				productUnitStock.total_update -= totalSai
				productUnitStock.total_out += totalSai
				productUnitStock.save()
				messages.success(request, f'Dadus Distribuisaun {product.name} GOTA rejista ona.')
				# return redirect('distribution-dash')
				return redirect('detail-production-list',productunit.id)
	else:
		form = ProductSellForm1()

	context = {
		"group":group,
		"title":"Rejista Distribuisaun Produtu GOTTA",
		"page":"form",
		"form":form,
		"productunit":productunit,
	}

	return render (request, 'distribution/dash.html',context)


@login_required
@allowed_users(allowed_roles=['admin','distribuicao'])
def ajax_load_product_price(request):
	unitId = request.GET.get('unit')
	unitData = ProductUnit.objects.get(id=unitId)
	return render(request, 'distribution/unitDataLoad.html', {'unitData': unitData})
