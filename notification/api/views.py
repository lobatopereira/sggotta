from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from client.models import Pedidu

# dir. munisipiu
class APINotifBadgeDist(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		obj1 = Pedidu.objects.filter(is_sent=True, is_ontheway=False).all().count()
		objects = obj1
		return Response({'value':objects})

class APINotifPediduFoun(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		obj1 = Pedidu.objects.filter(is_sent=True, is_ontheway=False).all().count()
		objects = obj1
		return Response({'value':objects})

# class APINotifImplementasaunDirMun(APIView):
# 	authentication_classes = [SessionAuthentication, BasicAuthentication]
# 	permission_classes = [IsAuthenticated]
# 	def get(self, request, format=None):
# 		diretor = c_user_fun(request.user)
# 		obj1 = ImplementasaunUKL.objects.filter(is_sent=True, is_approved=False,municipality__id=diretor.areamunicipality.id).all().count()
# 		objects = obj1
# 		return Response({'value':objects})

# # administrative post
# class APINotifBadgeFunPost(APIView):
# 	authentication_classes = [SessionAuthentication, BasicAuthentication]
# 	permission_classes = [IsAuthenticated]
# 	def get(self, request, format=None):
# 		fun = c_user_fun(request.user)
# 		obj1 = SurveyUKL.objects.filter(is_sent=False, is_approved=False, is_rejected=True,administrativepost__id=fun.areaadministrativepost.id).all().count()
# 		obj2 = ImplementasaunUKL.objects.filter(is_sent=False, is_approved=False, is_rejected=True,administrativepost__id=fun.areaadministrativepost.id).all().count()
# 		objects = obj1+obj2
# 		return Response({'value':objects})

# class APINotifSurveyRejeitaduFunPost(APIView):
# 	authentication_classes = [SessionAuthentication, BasicAuthentication]
# 	permission_classes = [IsAuthenticated]
# 	def get(self, request, format=None):
# 		fun = c_user_fun(request.user)
# 		obj1 = SurveyUKL.objects.filter(is_sent=False, is_approved=False, is_rejected=True,administrativepost__id=fun.areaadministrativepost.id).all().count()
# 		objects = obj1
# 		return Response({'value':objects})

# class APINotifImplementasaunRejeitaduFunPost(APIView):
# 	authentication_classes = [SessionAuthentication, BasicAuthentication]
# 	permission_classes = [IsAuthenticated]
# 	def get(self, request, format=None):
# 		fun = c_user_fun(request.user)
# 		obj1 = ImplementasaunUKL.objects.filter(is_sent=False, is_approved=False, is_rejected=True,administrativepost__id=fun.areaadministrativepost.id).all().count()
# 		objects = obj1
# 		return Response({'value':objects})