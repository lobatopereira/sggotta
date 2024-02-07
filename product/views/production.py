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

@login_required
@allowed_users(allowed_roles=['admin','producao'])
def ProductionDash(request):
	group = request.user.groups.all()[0].name
	objects = ProductUnitStock.objects.all()
	context = {
		"group":group,
		"title":"Painel Produsaun GOTTA",
		"page":"dash",
		"objects":objects,
		"active_pro":"active",
	}

	return render (request, 'production/dash.html',context)

@login_required
@allowed_users(allowed_roles=['admin','producao','distribuicao'])
def DetailProductionList(request,id):
	group = request.user.groups.all()[0].name
	objects1 = ProductUnit.objects.get(id=id)
	objects2 = ProductTransaction.objects.filter(unit=objects1).all().order_by('-id','date')
	# objects3 = ProductTransaction.objects.filter(unit=objects1).order_by('-date_created').last()
	# objects2 = objects2[: len(objects2) - 1] if objects2 else None
	for x in objects2:
		print("objects2:",x.total_in," ",x.total_out," ",x.total)
	print('objects2:',objects2)
	context = {
		"group":group,
		"title":f"Lista Produsaun {objects1.product.name} ({objects1.unit})",
		"page":"list",
		"objects1":objects1,
		"objects2":objects2,
		# "objects3":objects3,
		"active_pro":"active",
	}

	return render (request, 'production/dash.html',context)

@login_required
@allowed_users(allowed_roles=['admin','producao'])
def DetailProductionAdd(request,id):
	group = request.user.groups.all()[0].name
	objects1 = ProductUnit.objects.get(id=id)
	objects = Product.objects.get(id=objects1.product.id)
	if request.method == 'POST':
		form = ProductTransactionForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user_created = request.user
			instance.product = objects
			instance.unit = objects1
			totalTama = instance.total_in
			instance.total_out = 0
			lastTransantion = ProductTransaction.objects.filter(unit=objects1).order_by('id').last()
			if lastTransantion:
				print('lastTransantion:',lastTransantion)
				instance.total = lastTransantion.total + totalTama
			else:
				instance.total = 0 + totalTama
			newTotal = instance.total
			instance.save()
			productUnitStock = get_object_or_404(ProductUnitStock,unit=objects1,product=objects)
			productUnitStock.total = newTotal
			productUnitStock.total_update += totalTama
			if productUnitStock.total_update_pedidu is None:
				productUnitStock.total_update_pedidu = totalTama
			else:
				productUnitStock.total_update_pedidu += totalTama
			if lastTransantion:
				lastTransantion.is_confirm = True
				lastTransantion.save()
			productUnitStock.save()
			messages.success(request, f'Dadus Produsaun {objects.name} GOTA aumenta ona.')
			return redirect('detail-production-list',objects1.id)
	else:
		form = ProductTransactionForm()
	context = {
		"group":group,
		"title":f"Aumenta Produsaun {objects.name}",
		"page":"form",
		"form":form,
		"objects":objects,
		"objects1":objects1,
		"active_pro":"active",
	}

	return render (request, 'production/dash.html',context)


@login_required
@allowed_users(allowed_roles=['admin','producao'])
def deleteProProduction(request,id):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(ProductTransaction,id=id)
	unit = get_object_or_404(ProductUnit,id=objects.unit.id)
	stock = get_object_or_404(ProductUnitStock,unit=unit)
	totalDelete = objects.total_in
	stock.total = stock.total - totalDelete
	stock.total_update -= totalDelete
	objects.delete()
	stock.save()
	messages.error(request, f'Dadus Produsaun GOTA {objects.product.name}, {objects.unit.unit} {objects.total_in} apaga ona.')
	return redirect('detail-production-list',unit.id)

@login_required
@allowed_users(allowed_roles=['admin','producao'])
def confirmProProduction(request,id):
	group = request.user.groups.all()[0].name
	objects = get_object_or_404(ProductTransaction,id=id)
	unit = get_object_or_404(ProductUnit,id=objects.unit.id)
	objects.is_confirm = True
	objects.save()
	messages.success(request, f'Dadus Produsaun GOTA {objects.product.name}, {objects.unit.unit} {objects.total_in} konfirmadu ona.')
	return redirect('detail-production-list',unit.id)
