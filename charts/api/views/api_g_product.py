from django.shortcuts import render, redirect, get_object_or_404
import numpy as np
from django.db.models import Count, Q
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.models import User, Group
import datetime
from product.models import *
from reports.utils import getFulanNaran
from distribution.models import *
from datetime import date


class APIGProductStock(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request, format=None):
		group = request.user.groups.all()[0].name
		objects = ProductUnitStock.objects.all()
		label,obj = list(),list()
		for i in objects:
			obj.append(i.total_update)
			label.append(i.unit.product.name)
		data = { 'label': label, 'obj': obj, }
		return Response(data)

class APIGProductSumm(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request, format=None):
		group = request.user.groups.all()[0].name
		objects = ProductUnitStock.objects.all()
		if group == 'client':
			label,labels,obj = list(),list(['Total Stock']),list()
			for i in objects:
				obj.append([i.total_update_pedidu])
				label.append(i.unit.product.name)
		else:
			label,labels,obj = list(),list(['Total Produsaun','Total Stock','Total Sai']),list()
			for i in objects:
				obj.append([i.total,i.total_update,i.total_out])
				label.append(i.unit.product.name)
		data = { 'labels': labels, 'label': label, 'obj': obj, }
		return Response(data)

class APIGProductSummAll(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request, format=None):
		group = request.user.groups.all()[0].name
		total_produsaun = ProductUnitStock.objects.aggregate(total_sum=Sum('total'))['total_sum']
		total_distribuisaun = ProductUnitStock.objects.aggregate(total_sum=Sum('total_out'))['total_sum']
		total_stock = ProductUnitStock.objects.aggregate(total_sum=Sum('total_update'))['total_sum']
		label = ["Produsaun","Distribuisaun","Stock"]
		obj = [total_produsaun,total_distribuisaun,total_stock]
		data = { 'label': label, 'obj': obj }
		return Response(data)

class APIGProductSummByMonthThisYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request, format=None):
		group = request.user.groups.all()[0].name
		label,obj,labels = list(),list(),list()
		objects = ProductUnitStock.objects.all()
		monthListOrder = [1,2,3,4,5,6,7,8,9,10,11,12]
		listaProdutu = Product.objects.all()
		for x in listaProdutu:
			labels.append(x.name)
			# labels.append(getFulanNaran(x))
		for x in monthListOrder:
			obj_c_f_ass = []
			for i in listaProdutu:
				# distribuisaun = ProductSell.objects.filter(product__id=i.id,date__month=x,date__year=date.today().year).aggregate(total_sum=Sum('total_out'))['total_sum']
				# if distribuisaun == None:
				# 	distribuisaun = 0
				# else:
				# 	distribuisaun = distribuisaun
				produsaun = ProductTransaction.objects.filter(product__id=i.id,total_in__isnull=False,date__month=x,date__year=date.today().year).aggregate(total_sum=Sum('total_in'))['total_sum']
				if produsaun == None:
					produsaun = 0
				else:
					produsaun = produsaun
				obj_c_f_ass.append(produsaun)
			# label.append(i.name)
			label.append(getFulanNaran(x))
			obj.append(obj_c_f_ass)
		data = { 'labels': labels, 'label': label, 'obj': obj, }
		return Response(data)

class APIGDistributionSummByMonthThisYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request, format=None):
		group = request.user.groups.all()[0].name
		label,obj,labels = list(),list(),list()
		objects = ProductUnitStock.objects.all()
		monthListOrder = [1,2,3,4,5,6,7,8,9,10,11,12]
		listaProdutu = Product.objects.all()
		for x in listaProdutu:
			labels.append(x.name)
			# labels.append(getFulanNaran(x))
		for x in monthListOrder:
			obj_c_f_ass = []
			for i in listaProdutu:
				distribuisaun = ProductSell.objects.filter(product__id=i.id,date__month=x,date__year=date.today().year).aggregate(total_sum=Sum('total_out'))['total_sum']
				if distribuisaun == None:
					distribuisaun = 0
				else:
					distribuisaun = distribuisaun
				# produsaun = ProductTransaction.objects.filter(product__id=i.id,total_in__isnull=False,date__month=x,date__year=date.today().year).aggregate(total_sum=Sum('total_in'))['total_sum']
				# if produsaun == None:
				# 	produsaun = 0
				# else:
				# 	produsaun = produsaun
				obj_c_f_ass.append(distribuisaun)
			# label.append(i.name)
			label.append(getFulanNaran(x))
			obj.append(obj_c_f_ass)
		data = { 'labels': labels, 'label': label, 'obj': obj, }
		return Response(data)


class APIGProductSummByYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request, format=None):
		group = request.user.groups.all()[0].name
		label,obj,labels = list(),list(),list()
		objects = ProductUnitStock.objects.all()
		years = ProductTransaction.objects.distinct().values('date__year').all().order_by('date__year')
		listaProdutu = Product.objects.all()
		for x in listaProdutu:
			labels.append(x.name)
			# labels.append(getFulanNaran(x))
		for x in years:
			obj_c_f_ass = []
			for i in listaProdutu:
				produsaun = ProductTransaction.objects.filter(product__id=i.id,total_in__isnull=False,date__year=x['date__year']).aggregate(total_sum=Sum('total_in'))['total_sum']
				if produsaun == None:
					produsaun = 0
				else:
					produsaun = produsaun
				obj_c_f_ass.append(produsaun)
			# label.append(i.name)
			label.append(x['date__year'])
			obj.append(obj_c_f_ass)
		data = { 'labels': labels, 'label': label, 'obj': obj, }
		return Response(data)

class APIGDistributionSummByYear(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request, format=None):
		group = request.user.groups.all()[0].name
		label,obj,labels = list(),list(),list()
		objects = ProductUnitStock.objects.all()
		listaProdutu = Product.objects.all()
		years = ProductTransaction.objects.distinct().values('date__year').all().order_by('date__year')
		for x in listaProdutu:
			labels.append(x.name)
			# labels.append(getFulanNaran(x))
		for x in years:
			obj_c_f_ass = []
			for i in listaProdutu:
				distribuisaun = ProductSell.objects.filter(product__id=i.id,date__year=x['date__year']).aggregate(total_sum=Sum('total_out'))['total_sum']
				if distribuisaun == None:
					distribuisaun = 0
				else:
					distribuisaun = distribuisaun
				# produsaun = ProductTransaction.objects.filter(product__id=i.id,total_in__isnull=False,date__month=x,date__year=date.today().year).aggregate(total_sum=Sum('total_in'))['total_sum']
				# if produsaun == None:
				# 	produsaun = 0
				# else:
				# 	produsaun = produsaun
				obj_c_f_ass.append(distribuisaun)
			# label.append(i.name)
			label.append(x['date__year'])
			obj.append(obj_c_f_ass)
		data = { 'labels': labels, 'label': label, 'obj': obj, }
		return Response(data)

class APIGDistributionSummByMonthThisYearPrice(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request, format=None):
		group = request.user.groups.all()[0].name
		label,obj,labels = list(),list(),list()
		objects = ProductUnitStock.objects.all()
		monthListOrder = [1,2,3,4,5,6,7,8,9,10,11,12]
		listaProdutu = Product.objects.all()
		for x in listaProdutu:
			labels.append(x.name)
			# labels.append(getFulanNaran(x))
		for x in monthListOrder:
			obj_c_f_ass = []
			for i in listaProdutu:
				distribuisaun = ProductSell.objects.filter(product__id=i.id,date__month=x,date__year=date.today().year).aggregate(total_sum=Sum('totalprice'))['total_sum']
				if distribuisaun == None:
					distribuisaun = 0
				else:
					distribuisaun = distribuisaun
				# produsaun = ProductTransaction.objects.filter(product__id=i.id,total_in__isnull=False,date__month=x,date__year=date.today().year).aggregate(total_sum=Sum('total_in'))['total_sum']
				# if produsaun == None:
				# 	produsaun = 0
				# else:
				# 	produsaun = produsaun
				obj_c_f_ass.append(distribuisaun)
			# label.append(i.name)
			label.append(getFulanNaran(x))
			obj.append(obj_c_f_ass)
		data = { 'labels': labels, 'label': label, 'obj': obj, }
		return Response(data)