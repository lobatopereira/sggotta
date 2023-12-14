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
from datetime import date
from reports.utils import getFulanNaran,getFulanNumeru

# Create your views here.
@login_required
@allowed_users(allowed_roles=['diretor','admin','distribuicao','producao'])
def ReportDash(request):
	group = request.user.groups.all()[0].name
	listaProdutu = Product.objects.all()
	total_produsaun = ProductUnitStock.objects.aggregate(total_sum=Sum('total'))['total_sum']
	total_distribuisaun = ProductUnitStock.objects.aggregate(total_sum=Sum('total_out'))['total_sum']
	total_stock = ProductUnitStock.objects.aggregate(total_sum=Sum('total_update'))['total_sum']
	sumariuProdutu = []
	for x in listaProdutu.iterator():
		produsaun = ProductUnitStock.objects.filter(product__id=x.id).last()
		if produsaun:
			sumariuProdutu.append({'id':x.id,'name':x.name,'produsaun':produsaun.total,'distribuisaun':produsaun.total_out,'stock':produsaun.total_update})
		# distribusaun = ProductUnitStock.objects.get(product__id=x.id)
		# stock = ProductUnitStock.objects.get(product__id=x.id)

	monthListOrder = [1,2,3,4,5,6,7,8,9,10,11,12]
	sumariu_tuir_fulan_tinan_atual = []
	for x in monthListOrder:
		sumariuProdutuTuirFulan = []
		for i in listaProdutu:
			distribuisaun = ProductSell.objects.filter(product__id=i.id,date__month=x,date__year=date.today().year).aggregate(total_sum=Sum('total_out'))['total_sum']
			if distribuisaun == None:
				distribuisaun = 0
			else:
				distribuisaun = distribuisaun
			produsaun = ProductTransaction.objects.filter(product__id=i.id,total_in__isnull=False,date__month=x,date__year=date.today().year).aggregate(total_sum=Sum('total_in'))['total_sum']
			if produsaun == None:
				produsaun = 0
			else:
				produsaun = produsaun
			sumariuProdutuTuirFulan.append({"produtu":i.name,"produtuID":i.id,"distribuisaun":distribuisaun,"produsaun":produsaun})
		sumariu_tuir_fulan_tinan_atual.append({
			"fulan":getFulanNaran(x),
			"idFulan":x,
			"sumariuProdutuTuirFulan":sumariuProdutuTuirFulan,
			})

	years = ProductTransaction.objects.distinct().values('date__year').all().order_by('date__year')
	sumario_kada_tinan = []
	for x in years:
		sumariuProdutuTuirTinan = []
		for i in listaProdutu:
			distribuisaun = ProductSell.objects.filter(product__id=i.id,date__year=x['date__year']).aggregate(total_sum=Sum('total_out'))['total_sum']
			if distribuisaun == None:
				distribuisaun = 0
			else:
				distribuisaun = distribuisaun
			produsaun = ProductTransaction.objects.filter(product__id=i.id,total_in__isnull=False,date__year=x['date__year']).aggregate(total_sum=Sum('total_in'))['total_sum']
			if produsaun == None:
				produsaun = 0
			else:
				produsaun = produsaun
			sumariuProdutuTuirTinan.append({"produtu":i.name,"produtuID":i.id,"distribuisaun":distribuisaun,"produsaun":produsaun})
		sumario_kada_tinan.append({
			"tinan":x['date__year'],
			"sumariuProdutuTuirTinan":sumariuProdutuTuirTinan,
			})

	context = {
		"title":"Relatoriu Tabular Produtu GOTTA",
		"active_relatoriu":"active",
		"listaProdutu":listaProdutu,
		"sumariu_tuir_fulan_tinan_atual":sumariu_tuir_fulan_tinan_atual,
		"sumario_kada_tinan":sumario_kada_tinan,
		"sumariuProdutu":sumariuProdutu,
		"total_produsaun":total_produsaun,
		"total_distribuisaun":total_distribuisaun,
		"total_stock":total_stock,
	}
	return render(request, "tabular/DashTabularReport.html",context)
	# return render(request, "tabular/DashTabularReport.html")

@login_required
@allowed_users(allowed_roles=['diretor','admin','distribuicao','producao'])
def reportProdusaun(request,hashid):
	group = request.user.groups.all()[0].name
	objects = Product.objects.get(id=hashid)
	produsaun = ProductUnitStock.objects.get(product__id=objects.id)
	objects1 = ProductTransaction.objects.filter(product=objects).exclude(total_in=0)

	context = {
		"title":f"Relatoriu Produsaun Produtu GOTTA ({objects.name})",
		"active_relatoriu":"active",
		"produsaun":produsaun,
		"objects1":objects1,
		"objects":objects,
	}
	return render(request, "tabular/ProductionReport.html",context)

@login_required
@allowed_users(allowed_roles=['diretor','admin','distribuicao','producao'])
def reportDistribuicao(request,hashid):
	group = request.user.groups.all()[0].name
	objects = Product.objects.get(id=hashid)
	produsaun = ProductUnitStock.objects.get(product__id=objects.id)
	objects1 = ProductTransaction.objects.filter(product=objects).exclude(total_out=0)

	context = {
		"title":f"Relatoriu Distribuisaun Produtu GOTTA ({objects.name})",
		"active_relatoriu":"active",
		"produsaun":produsaun,
		"objects1":objects1,
		"objects":objects,
	}
	return render(request, "tabular/DistributionReport.html",context)


@login_required
@allowed_users(allowed_roles=['diretor','admin','distribuicao','producao'])
def reportProdusaunTuirFulan(request,hashid,hashid1):
	group = request.user.groups.all()[0].name
	fulan = getFulanNumeru(hashid1)
	objects = Product.objects.get(id=hashid)
	produsaun = ProductUnitStock.objects.get(product__id=objects.id)
	objects1 = ProductTransaction.objects.filter(product=objects,date__month=fulan,date__year=date.today().year).exclude(total_in=0)

	context = {
		"title":f"Relatoriu Produsaun Produtu GOTTA ({objects.name}) iha Fulan {hashid1}",
		"active_relatoriu":"active",
		"produsaun":produsaun,
		"objects1":objects1,
		"objects":objects,
	}
	return render(request, "tabular/ProductionReport.html",context)

@login_required
@allowed_users(allowed_roles=['diretor','admin','distribuicao','producao'])
def reportDistribuicaoTuirFulan(request,hashid,hashid1):
	group = request.user.groups.all()[0].name
	fulan = getFulanNumeru(hashid1)
	objects = Product.objects.get(id=hashid)
	produsaun = ProductUnitStock.objects.get(product__id=objects.id)
	objects1 = ProductSell.objects.filter(product__id=objects.id,date__month=fulan,date__year=date.today().year).exclude(total_out=0)

	context = {
		"title":f"Relatoriu Distribuisaun Produtu GOTTA ({objects.name}) iha Fulan {hashid1}",
		"active_relatoriu":"active",
		"produsaun":produsaun,
		"objects1":objects1,
		"objects":objects,
	}
	return render(request, "tabular/DistributionReport.html",context)

@login_required
@allowed_users(allowed_roles=['diretor','admin','distribuicao','producao'])
def reportProdusaunTuirTinan(request,hashid,hashid1):
	group = request.user.groups.all()[0].name
	objects = Product.objects.get(id=hashid)
	produsaun = ProductUnitStock.objects.get(product__id=objects.id)
	objects1 = ProductTransaction.objects.filter(product=objects,date__year=hashid1).exclude(total_in=0)

	context = {
		"title":f"Relatoriu Produsaun Produtu GOTTA ({objects.name}) iha Tinan {hashid1}",
		"active_relatoriu":"active",
		"produsaun":produsaun,
		"objects1":objects1,
		"objects":objects,
	}
	return render(request, "tabular/ProductionReport.html",context)

@login_required
@allowed_users(allowed_roles=['diretor','admin','distribuicao','producao'])
def reportDistribuicaoTuirTinan(request,hashid,hashid1):
	group = request.user.groups.all()[0].name
	objects = Product.objects.get(id=hashid)
	produsaun = ProductUnitStock.objects.get(product__id=objects.id)
	objects1 = ProductSell.objects.filter(product__id=objects.id,date__year=hashid1).exclude(total_out=0)

	context = {
		"title":f"Relatoriu Distribuisaun Produtu GOTTA ({objects.name}) iha Fulan {hashid1}",
		"active_relatoriu":"active",
		"produsaun":produsaun,
		"objects1":objects1,
		"objects":objects,
	}
	return render(request, "tabular/DistributionReport.html",context)