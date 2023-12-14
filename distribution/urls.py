from django.urls import path
from . import views

urlpatterns = [
    path('dash/', views.DistDash, name="distribution-dash"),
    path('Out/Add/', views.DistOutAdd, name="distribution-out-add"),
    path('Out/Add/<str:id>', views.ProductDistOutAdd, name="product-distribution-out-add"),
    
    # pedidu
    path('product-request/list/', views.ProductRequestList, name="product-request-list"),
    path('dist/request/detail/<str:hashid>', views.DistRequestDetail, name="dist-detallu-pedidu"),
    path('dist/request/has-delivered/<str:hashid>', views.DistRequestProductDelivered, name="dist-konfirma-entrega-ona-produtu"),

    path('ajax/load/product-unit-price/', views.ajax_load_product_price, name='ajax_load_product_price'),
 
]