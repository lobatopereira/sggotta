from django.shortcuts import render,redirect, get_object_or_404,HttpResponse
from django.http import HttpResponse
from django.contrib.auth.models import User,Group
from custom.utils import *
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from users.utils import c_user_client
from client.models import *
from client.forms import *
from users.models import Profile
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
# from ipware import get_client_ip
# from ip2geotools.databases.noncommercial import DbIpCity
import datetime
from django.contrib import messages
from django.db import transaction

@login_required
@allowed_users(allowed_roles=['client'])
def ClientProductRequestList(request):
	group = request.user.groups.all()[0].name
	client = c_user_client(request.user)
	objects = ProductUnitStock.objects.all()
	objects1 = Pedidu.objects.filter(client=client,is_delivered=False)
	context = {
		"title":"Dashboard Produtu GOTTA",
		"page":"dash",
		"objects":objects,
		"objects1":objects1,
		"client":client,
		"group":group,
	}

	return render (request, 'pedidu/dash.html',context)

@login_required
@allowed_users(allowed_roles=['client'])
def ClientProductRequestHistoryList(request):
	group = request.user.groups.all()[0].name
	client = c_user_client(request.user)
	objects1 = Pedidu.objects.filter(client=client,is_delivered=True)
	context = {
		"title":"Historia Pedidu Produtu GOTTA",
		"page":"historylist",
		"objects1":objects1,
		"client":client,
		"group":group,
	}

	return render (request, 'pedidu/dash.html',context)

@login_required
@allowed_users(allowed_roles=['client'])
def ClientProductRequestAdd(request):
	group = request.user.groups.all()[0].name
	productobjects = ProductUnitStock.objects.filter(total_update_pedidu__gt=1)
	client = c_user_client(request.user)
	if request.method == 'POST':
		newid = getjustnewid(Pedidu)
		new_hashid = hash_md5(str(newid))
		with transaction.atomic():
			datapedidu = request.POST.get("datapedidu")
			produtu = request.POST.getlist("produtu")
			totalpedidu = request.POST.getlist("totalpedidu")
			createPedidu = Pedidu.objects.create(id=newid,hashed=new_hashid,client=client,datapedidu=datapedidu)
			for x,y in zip(produtu,totalpedidu):
				newid1 = getjustnewid(PediduProdutu)
				new_hashid1 = hash_md5(str(newid1))
				produtuData = get_object_or_404(ProductUnitStock,id=x)
				unitprice = produtuData.unit.price * int(y)
				if int(y) >= produtuData.total_update_pedidu:
					PediduProdutu.objects.create(id=newid1,hashed=new_hashid1,unit=produtuData.unit,product=produtuData.product,\
						totalprodutu=y,pedidu=createPedidu,totalpresu=unitprice)
					produtuData.total_update_pedidu -= int(y)
					produtuData.save() 
					messages.success(request, f'Pedidu Foun ba Produtu GOTA Rejista ona.')
				else:
					messages.success(request, f'Total Pedidu nebe ita boot haruka, montante boot Produtu nebe disponivel.')
			return redirect('client-product-request-list')
	context = {
		"title":"Rejista Pedidu Foun",
		"page":"form",
		"productobjects":productobjects,
		"group":group,
	}
	return render (request, 'pedidu/dash.html',context)

@login_required
@allowed_users(allowed_roles=['client'])
def ClientProductRequestAdd1(request,hashid):
	group = request.user.groups.all()[0].name
	client = c_user_client(request.user)
	pedidu = get_object_or_404(Pedidu,hashed=hashid)
	productobjects = ProductUnitStock.objects.filter(total_update_pedidu__gt=1)
	if request.method == 'POST':
		newid = getjustnewid(PediduProdutu)
		new_hashid = hash_md5(str(newid))
		with transaction.atomic():
			produtu = request.POST.get("produtu")
			totalpedidu = request.POST.get("totalpedidu")
			produtuData = get_object_or_404(ProductUnitStock,id=produtu)
			unitprice = produtuData.unit.price * int(totalpedidu) 
			if int(totalpedidu) <= produtuData.total_update_pedidu:
				PediduProdutu.objects.create(id=newid,hashed=new_hashid,unit=produtuData.unit,product=produtuData.product,\
							totalprodutu=totalpedidu,pedidu=pedidu,totalpresu=unitprice)
				produtuData.total_update_pedidu -= int(totalpedidu)
				produtuData.save() 
				messages.success(request, f'Pedidu ba Produtu GOTA Rejista ona.')
			else:
				messages.warning(request, f'Deskulpa, Total Pedidu ba Produtu nebe ita boot halo barak liu stock.')

			return redirect('client-product-request-detail',pedidu.hashed)
	context = {
		"title":"Rejista Pedidu ba Produtu GOTA",
		"page":"form1",
		"productobjects":productobjects,
		"group":group,
		"pedidu":pedidu,
	}
	return render (request, 'pedidu/dash.html',context)

@login_required
@allowed_users(allowed_roles=['client'])
def ClientProductItemRequestUpdate(request,hashid):
	group = request.user.groups.all()[0].name
	client = c_user_client(request.user)
	pediduprodutu = get_object_or_404(PediduProdutu,hashed=hashid)
	pedidu = get_object_or_404(Pedidu,hashed=pediduprodutu.pedidu.hashed)
	productobjects = ProductUnitStock.objects.get(product=pediduprodutu.product,unit=pediduprodutu.unit)
	if request.method == 'POST':
		with transaction.atomic():
			produtu = request.POST.get("produtu")
			print("produtu:",produtu)
			totalpedidu = request.POST.get("totalpedidu")
			produtuData = get_object_or_404(ProductUnitStock,id=produtu)
			PediduProdutu.objects.filter(id=pediduprodutu.id,hashed=pediduprodutu.hashed,pedidu=pedidu).update(totalprodutu=totalpedidu)
			previousTotal = int(pediduprodutu.totalprodutu)
			updatedTotal = int(totalpedidu)
			diff = abs(int(previousTotal)-int(updatedTotal))
			if previousTotal > updatedTotal:
				produtuData.total_update_pedidu += int(diff)
			elif previousTotal < updatedTotal:
				produtuData.total_update_pedidu -= int(diff)
			produtuData.save() 
			messages.success(request, f'Pedidu ba Produtu GOTA Rejista ona.')
			return redirect('client-product-request-detail',pedidu.hashed)
	context = {
		"title":"Rejista Pedidu ba Produtu GOTA",
		"page":"form1update",
		"productobjects":productobjects,
		"group":group,
		"pedidu":pedidu,
		"pediduprodutu":pediduprodutu,
	}
	return render (request, 'pedidu/dash.html',context)

@login_required
@allowed_users(allowed_roles=['client'])
def ClientProductRequestDelete(request,id):
	group = request.user.groups.all()[0].name
	client = c_user_client(request.user)
	pedidu = Pedidu.objects.get(id=id)
	pediduprodutuData = PediduProdutu.objects.filter(pedidu=pedidu)
	with transaction.atomic():
		for x in pediduprodutuData:
			produtuData = get_object_or_404(ProductUnitStock,unit=x.unit,product=x.product)
			produtuData.total_update_pedidu += x.totalprodutu
			produtuData.save()
		pedidu.delete()
	messages.success(request, f'Dadus Pedidu ba Produtu GOTA iha Data {pedidu.datapedidu} delete ona.')
	return redirect('client-product-request-list')

@login_required
@allowed_users(allowed_roles=['client'])
def ClientProductRequestListSend(request,hashid):
	group = request.user.groups.all()[0].name
	client = c_user_client(request.user)
	pedidu = Pedidu.objects.get(hashed=hashid)
	with transaction.atomic():
		pedidu.is_sent = True
		pedidu.save()
	messages.success(request, f'Ita boot nia Pedidu ba Produtu GOTA manda ona.')
	return redirect('client-product-request-detail', pedidu.hashed)

@login_required
@allowed_users(allowed_roles=['client'])
def ClientProductRequestDelete1(request,id):
	group = request.user.groups.all()[0].name
	client = c_user_client(request.user)
	# pedidu = Pedidu.objects.get(id=id)
	pediduprodutuData = PediduProdutu.objects.get(id=id)
	with transaction.atomic():
		produtuData = get_object_or_404(ProductUnitStock,unit=pediduprodutuData.unit,product=pediduprodutuData.product)
		produtuData.total_update_pedidu += pediduprodutuData.totalprodutu
		produtuData.save()
		pediduprodutuData.delete()
	messages.success(request, f'Dadus Pedidu ba Produtu {pediduprodutuData.product.name} delete ona.')
	return redirect('client-product-request-detail',pediduprodutuData.pedidu.hashed)

@login_required
@allowed_users(allowed_roles=['client'])
def ClientProductRequestDetail(request,hashid):
	group = request.user.groups.all()[0].name
	client = c_user_client(request.user)
	objects = ProductUnitStock.objects.all()
	objects1 = Pedidu.objects.get(hashed=hashid)
	context = {
		"title":"Detallu Pedidu Produtu GOTTA",
		"page":"detail",
		"objects":objects,
		"objects1":objects1,
		"client":client,
		"group":group,
	}

	return render (request, 'pedidu/dash.html',context)


