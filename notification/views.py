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
import datetime
from django.contrib import messages
from django.db import transaction
import qrcode
import base64
from io import BytesIO

@login_required
@allowed_users(allowed_roles=['distribuicao'])
def NotifListaPediduFoun(request):
	objects1 = Pedidu.objects.filter(is_sent=True, is_ontheway=False).all()
	context = {
		"title":"Lista Pedidu Produtu GOTTA husi Kliente sira",
		"page":"list",
		"objects1":objects1,
	}

	return render (request, 'distribution/notif/list.html',context)

@login_required
@allowed_users(allowed_roles=['distribuicao'])
def NotifDetalluPediduFoun(request,hashid):
	objects = Pedidu.objects.get(hashed=hashid)
	listaProdutu = PediduProdutu.objects.filter(pedidu=objects)
	allcheck = 0
	for x in listaProdutu:
		if x.is_checked == False:
			allcheck += 1
	context = {
		"title":f"Detallu Pedidu Produtu GOTTA husi Kliente {objects.client.firstname} {objects.client.lastname}",
		"page":"detail",
		"objects":objects,
		"allcheck":allcheck,
	}

	return render (request, 'distribution/notif/list.html',context)


@login_required
@allowed_users(allowed_roles=['distribuicao'])
def DistCheckRequestItem(request,hashid):
	group = request.user.groups.all()[0].name
	requestItem = PediduProdutu.objects.get(hashed=hashid)
	with transaction.atomic():
		unitPrice = ProductUnit.objects.filter(id=requestItem.unit.id).last()
		requestItem.totalpresu = float(float(unitPrice.price) * int(requestItem.totalprodutu))
		requestItem.is_checked = True
		requestItem.save()
	messages.success(request, f'Dadus Pedidu ba Produtu GOTA {requestItem.product.name} {requestItem.totalprodutu} {requestItem.unit.unit} konfirmadu ona.')
	return redirect('detallu-pedidu-foun-husi-cliente',requestItem.pedidu.hashed)

@login_required
@allowed_users(allowed_roles=['distribuicao'])
def DistDistribuiitemRequest(request,hashid):
	group = request.user.groups.all()[0].name
	requestItem = Pedidu.objects.get(hashed=hashid)
	with transaction.atomic():
		requestItem.is_ontheway = True
		requestItem.save()
	messages.success(request, f'Dadus Pedidu ba Produtu GOTA husi Kliente {requestItem.client.firstname} haruka ona.')
	return redirect('detallu-pedidu-foun-husi-cliente',requestItem.hashed)


from django.templatetags.static import static
import os
from PIL import Image
@login_required
@allowed_users(allowed_roles=['distribuicao','client'])
def DistPrintRequestItemNote(request,hashid):
	import datetime
	today = datetime.datetime.today()
	objects = Pedidu.objects.get(hashed=hashid)
	requestItemList = []
	totalprice = 0.0 
	listaPediduProdutu = PediduProdutu.objects.filter(pedidu=objects)
	print("listaPediduProdutu:",listaPediduProdutu)
	for x in listaPediduProdutu:
		requestItemList.append({"Produtu: ":x.product.name," Total Pedidu :":x.totalprodutu," Total Presu: ":x.totalpresu})
		totalprice = float(totalprice) + float(x.totalpresu)
	transaction_data = {
		'Kompanhia':"GOTA",
		'Data Pedidu':objects.datapedidu,
		'Kliente':str(objects.client.firstname)+str(" ")+str(objects.client.lastname),
		'Kontaktu':objects.client.phone,
		'enderesu':objects.client.address,
		'enderesu':objects.client.address,
		'Lista Pedidu Produtu':requestItemList,
		'Total Presu ikus':totalprice
	}
	qr = qrcode.QRCode(
		version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_L,
		box_size=20,
		border=4,
	)
	qr.add_data(str(transaction_data))
	qr.make(fit=True)
	qr_image = qr.make_image(fill_color="black", back_color="white")
	qr_image = qr_image.convert("RGBA")

	logo_path = os.path.join("static/main/images/gota.png")
	logo = Image.open(logo_path)
	logo = logo.resize((180, 180))

	qr_width, qr_height = qr_image.size
	logo_width, logo_height = logo.size
	position = ((qr_width - logo_width) // 2, (qr_height - logo_height) // 2)
	qr_image.paste(logo, position)

	buffered = BytesIO()
	qr_image.save(buffered, format="PNG")
	qr_image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

	context = {
		"title":f"Nota Pedidu Produtu GOTTA husi Kliente {objects.client.firstname} {objects.client.lastname}",
		"page":"detail",
		"objects":objects,
		"today":today,
		"listaPediduProdutu":listaPediduProdutu,
		"qr_image_base64":qr_image_base64,
	}

	return render (request, 'distribution/nota/impriminotapedidu.html',context)




