from django.shortcuts import render,redirect, get_object_or_404,HttpResponse
from django.http import HttpResponse
from django.contrib.auth.models import User,Group
from custom.utils import *
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from product.models import *
from product.forms import *
# from ipware import get_client_ip
# from ip2geotools.databases.noncommercial import DbIpCity
import datetime
from django.contrib import messages

# Create your views here.

@login_required
@allowed_users(allowed_roles=['admin'])
def ProductList(request):
	objects = Product.objects.all()
	context = {
		"title":"Lista Produtu GOTTA",
		"page":"list",
		"objects":objects,
	}

	return render (request, 'product/custom_list.html',context)

@login_required
@allowed_users(allowed_roles=['admin'])
def ProductAdd(request):
	if request.method == 'POST':
		form = ProductForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = datetime.datetime.now()
			instance.user_created = request.user
			instance.save()
			messages.success(request, f'Produtu Foun GOTA aumenta ona.')
			return redirect('product')
	else:
		form = ProductForm()
	context = {
		"title":"Rejista Produtu GOTTA",
		"page":"form",
		"form":form,
	}

	return render (request, 'product/custom_list.html',context)

@login_required
@allowed_users(allowed_roles=['admin'])
def ProductUpdate(request,id):
	objects = get_object_or_404(Product,id=id)
	if request.method == 'POST':
		form = ProductForm(request.POST, request.FILES,instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, f'Produtu GOTA altera ona.')
			return redirect('product')
	else:
		form = ProductForm(instance=objects)
	context = {
		"title":"Altera Produtu GOTTA",
		"page":"form",
		"form":form,
	}

	return render (request, 'product/custom_list.html',context)

@login_required
@allowed_users(allowed_roles=['admin'])
def ProductDetail(request,id):
	objects = get_object_or_404(Product,id=id)
	objects1 = ProductUnit.objects.filter(product=objects)
	context = {
		"title":f"Detalu Produtu {objects.name} GOTTA",
		"page":"detail",
		"objects":objects,
		"objects1":objects1,
	}

	return render (request, 'product/custom_list.html',context)

@login_required
@allowed_users(allowed_roles=['admin'])
def ProductDelete(request,id):
	objects = get_object_or_404(Product,id=id)
	objects.delete()
	messages.error(request, f'Produtu GOTA {objects.name} apaga ona.')
	return redirect('product')

@login_required
@allowed_users(allowed_roles=['admin'])
def ProductUnitAdd(request,id):
	objects = get_object_or_404(Product,id=id)
	if request.method == 'POST':
		form = ProductUnitForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.datetime = datetime.datetime.now()
			instance.user_created = request.user
			instance.product = objects
			instance.save()
			messages.success(request, f'Unidade Produtu {objects.name} GOTA aumenta ona.')
			return redirect('detailProduct',objects.id)
	else:
		form = ProductUnitForm()
	context = {
		"title":f"Rejista Unidade Produtu {objects.name} GOTTA",
		"page":"form",
		"form":form,
		"objects":objects,
	}

	return render (request, 'product/custom_list.html',context)

@login_required
@allowed_users(allowed_roles=['admin'])
def ProductUnitUpdate(request,id):
	objects = get_object_or_404(ProductUnit,id=id)
	if request.method == 'POST':
		form = ProductUnitForm(request.POST, request.FILES,instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, f'Unidade Produtu {objects.product.name} GOTA aumenta ona.')
			return redirect('detailProduct',objects.product.id)
	else:
		form = ProductUnitForm(instance=objects)
	context = {
		"title":f"Altera Unidade Produtu {objects.product.name} GOTTA",
		"page":"form",
		"form":form,
		"objects":objects,
	}

	return render (request, 'product/custom_list.html',context)

@login_required
@allowed_users(allowed_roles=['admin'])
def ProductUnitDelete(request,id):
	objects = get_object_or_404(ProductUnit,id=id)
	objects.delete()
	messages.error(request, f'Produtu GOTA {objects.product.name} unidade {objects.unit} apaga ona.')
	return redirect('detailProduct',objects.product.id)

@login_required
@allowed_users(allowed_roles=['admin'])
def deactivateProductUnit(request,id):
	objects = get_object_or_404(ProductUnit,id=id)
	objects.is_active = False
	objects.save()
	messages.error(request, f'Produtu GOTA {objects.product.name} unidade {objects.unit} dezativa ona.')
	return redirect('detailProduct',objects.product.id)

@login_required
@allowed_users(allowed_roles=['admin'])
def activateProductUnit(request,id):
	objects = get_object_or_404(ProductUnit,id=id)
	objects.is_active = True
	objects.save()
	messages.success(request, f'Produtu GOTA {objects.product.name} unidade {objects.unit} ativa ona.')
	return redirect('detailProduct',objects.product.id)




