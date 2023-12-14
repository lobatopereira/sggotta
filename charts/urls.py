from django.urls import path
from . import views

urlpatterns = [
    path('a/dashboard', views.ADashCharts, name="a-charts-dash"),

 
]