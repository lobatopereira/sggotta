from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.ClientList, name="client-list"),
    path('add/', views.ClientAdd, name="client-add"),
    path('update/<str:hashid>', views.ClientUpdate, name="client-update"),
    path('delete/<str:id>', views.ClientDelete, name="client-delete"),
    path('detail/<str:hashid>', views.ClientDetail, name="client-detail"),
 
    path('product/request/list/', views.ClientProductRequestList, name="client-product-request-list"),
    path('product/request/add/', views.ClientProductRequestAdd, name="client-product-request-add"),
    path('product/request/delete/<str:id>', views.ClientProductRequestDelete, name="client-product-request-delete"),
    path('product/request/detail/<str:hashid>', views.ClientProductRequestDetail, name="client-product-request-detail"),
    
    path('product/request/delete/item/<str:id>', views.ClientProductRequestDelete1, name="client-product-request-delete1"),
    path('product/item/request/add/<str:hashid>', views.ClientProductRequestAdd1, name="client-product-request-add1"),
    path('product/item/request/update/<str:hashid>', views.ClientProductItemRequestUpdate, name="client-product-item-request-update"),
    
    path('product/request/list/send/<str:hashid>', views.ClientProductRequestListSend, name="client-product-request-list-send"),
    
    path('product/request/history/list/', views.ClientProductRequestHistoryList, name="client-product-request-history-list"),
]