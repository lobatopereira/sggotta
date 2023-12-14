from django.shortcuts import render,redirect, get_object_or_404,HttpResponse
from django.http import HttpResponse
from django.contrib.auth.models import User,Group
from custom.utils import *
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
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
@allowed_users(allowed_roles=['admin','distribuicao'])
def ClientList(request):
	objects = Client.objects.all()
	context = {
		"title":"Lista Kliente GOTTA",
		"page":"list",
		"objects":objects,
	}

	return render (request, 'client/list.html',context)

@login_required
@allowed_users(allowed_roles=['admin','distribuicao'])
def ClientDetail(request,hashid):
	objects = Client.objects.get(id=hashid)
	context = {
		"title":"Informasaun Detallu Kliente",
		"page":"detail",
		"objects":objects,
	}

	return render (request, 'client/list.html',context)

@login_required
@allowed_users(allowed_roles=['admin','distribuicao'])
def ClientAdd(request):
	if request.method == 'POST':
		# newid = getjustnewid(Client)
		# new_hashid = hash_md5(str(newid))
		form = ClientForm(request.POST, request.FILES)
		if form.is_valid():
			with transaction.atomic():
				instance = form.save(commit=False)
				instance.datetime = datetime.datetime.now()
				instance.user_created = request.user
				instance.save()
				username = str(instance.firstname)+str(instance.lastname)
				password = make_password('password')
				obj2 = User(username=username, password=password,is_active=False)
				obj2.save()
				# clientData = get_object_or_404(Client,id=instance.id)
				ClientUser.objects.create(client=instance,user=obj2)
				# Profile.objects.create(user=obj2,firstname=instance.firstname,lastname=instance.lastname,pob=instance.pob,dob=instance.dob,sex=instance.sex,is_active=instance.is_active,image=instance.image,datetime=datetime.datetime.now(),user_created=request.user)
				group_user = Group.objects.get(name="client")
				user = User.objects.get(pk=obj2.id)
				user.groups.add(group_user)
				messages.success(request, f'Kliente Foun GOTA aumenta ona.')
				return redirect('client-list')
	else:
		form = ClientForm()
	context = {
		"title":"Rejista Kliente GOTTA",
		"page":"form",
		"form":form,
	}

	return render (request, 'client/list.html',context)

@login_required
@allowed_users(allowed_roles=['admin','distribuicao'])
def ClientUpdate(request,hashid):
	objects = get_object_or_404(Client,id=hashid)
	if request.method == 'POST':
		form = ClientForm(request.POST, request.FILES,instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, f'Dadus Kliente GOTA altera ona.')
			return redirect('client-list')
	else:
		form = ClientForm(instance=objects)
	context = {
		"title":"Altera Kliente GOTTA",
		"page":"form",
		"form":form,
	}

	return render (request, 'client/list.html',context)

@login_required
@allowed_users(allowed_roles=['admin'])
def ClientDelete(request,id):
	objects = get_object_or_404(Client,id=id)
	objects.delete()
	messages.error(request, f'Kliente GOTA ho naran {objects.firstname} {objects.lastname} apaga ona.')
	return redirect('client-list')
