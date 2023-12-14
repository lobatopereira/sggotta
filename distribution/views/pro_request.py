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
def ProductRequestList(request):
	group = request.user.groups.all()[0].name
	objects = Pedidu.objects.filter(is_ontheway=True)
	context = {
		"group":group,
		"title":"Dadus Pedidu ba Produtu GOTTA",
		"page":"list",
		"objects":objects,
	}

	return render (request, 'request/dash.html',context)

@login_required
@allowed_users(allowed_roles=['admin','distribuicao'])
def DistRequestDetail(request,hashid):
	group = request.user.groups.all()[0].name
	objects1 = Pedidu.objects.get(hashed=hashid)
	context = {
		"group":group,
		"title":"Detallu Pedidu ba Produtu GOTTA",
		"page":"detail",
		"objects1":objects1,
	}

	return render (request, 'request/dash.html',context)

@login_required
@allowed_users(allowed_roles=['admin','distribuicao'])
def DistRequestProductDelivered(request,hashid):
	group = request.user.groups.all()[0].name
	objects1 = Pedidu.objects.get(hashed=hashid)
	pediduprodutuData = PediduProdutu.objects.filter(pedidu=objects1)
	with transaction.atomic():
		objects1.is_delivered = True
		objects1.save()
		for x in pediduprodutuData:
			obj2 = get_object_or_404(PediduProdutu,id=x.id)
			obj2.is_delivered = True
			obj2.save()
			ProductSell.objects.create(client=objects1.client,product=obj2.product,unit=obj2.unit,date=objects1.datapedidu,total_out=obj2.totalprodutu,totalprice=obj2.totalpresu,user_created=request.user)
			productunit = ProductUnit.objects.get(id=obj2.unit.id)
			lastTransantion = ProductTransaction.objects.filter(unit=productunit).order_by('id').last()
			if lastTransantion:
				totalupdated = lastTransantion.total - obj2.totalprodutu
			else:
				messages.warning(request, f'Dadus Produsaun {product.name} GOTA Seidauk iha.')
				return redirect('distribution-dash')
			ProductTransaction.objects.create(date=objects1.datapedidu,total_in=0,total_out=obj2.totalprodutu,total=totalupdated,user_created=request.user,unit=productunit,product=obj2.product)
			productUnitStock = get_object_or_404(ProductUnitStock,unit=productunit,product=obj2.product)
			productUnitStock.total_update -= obj2.totalprodutu
			productUnitStock.total_out += obj2.totalprodutu
			productUnitStock.save()
		return redirect('dist-detallu-pedidu',objects1.hashed)


	