from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.ProductList, name="product"),
    path('add/', views.ProductAdd, name="ProductAdd"),
    path('update/<str:id>', views.ProductUpdate, name="updateProduct"),
    path('detail/<str:id>', views.ProductDetail, name="detailProduct"),
    path('delete/<str:id>', views.ProductDelete, name="deleteProduct"),
    path('unit/add/<str:id>', views.ProductUnitAdd, name="ProductUnitAdd"),
    path('unit/update/<str:id>', views.ProductUnitUpdate, name="updateProductUnit"),
    path('unit/delete/<str:id>', views.ProductUnitDelete, name="deleteProductUnit"),
    path('unit/deactivate/<str:id>', views.deactivateProductUnit, name="deactivateProductUnit"),
    path('unit/activate/<str:id>', views.activateProductUnit, name="activateProductUnit"),
    
    path('production/dash', views.ProductionDash, name="production-dash"),
    path('detail/production/list/<str:id>', views.DetailProductionList, name="detail-production-list"),
    path('detail/production/add/<str:id>', views.DetailProductionAdd, name="pro-production-add"),
    path('detail/production/delete/<str:id>', views.deleteProProduction, name="deleteProProduction"),
    path('detail/production/confirm/<str:id>', views.confirmProProduction, name="pro-production-confirm"),
]