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
from reports.utils import getFulanNaran

@login_required
@allowed_users(allowed_roles=['admin','diretor','distribuicao','producao'])
def ADashCharts(request):
	group = request.user.groups.all()[0].name
	total_produsaun = ProductUnitStock.objects.aggregate(total_sum=Sum('total'))['total_sum']
	total_distribuisaun = ProductUnitStock.objects.aggregate(total_sum=Sum('total_out'))['total_sum']
	total_stock = ProductUnitStock.objects.aggregate(total_sum=Sum('total_update'))['total_sum']
	context ={
		"total_produsaun":total_produsaun,
		"total_distribuisaun":total_distribuisaun,
		"total_stock":total_stock,
		"title":f"Pajina Relatoriu ho formatu Grafiku",
	}
	return render(request, "chart_a/dash.html",context)

