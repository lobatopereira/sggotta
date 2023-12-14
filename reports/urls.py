from django.urls import path
from . import views

urlpatterns = [
    path('dash/', views.ReportDash, name="ReportDash"),
    path('report/product/production/<str:hashid>', views.reportProdusaun, name="reportProdusaun"),
    path('report/product/distribution/<str:hashid>', views.reportDistribuicao, name="reportDistribuicao"),
    # path('Out/Add/<str:id>', views.ProductDistOutAdd, name="product-distribution-out-add"),
    path('report/product/production/<str:hashid>/month/<str:hashid1>', views.reportProdusaunTuirFulan, name="reportProdusaunTuirFulan"),
    path('report/product/distribution/<str:hashid>/month/<str:hashid1>', views.reportDistribuicaoTuirFulan, name="reportDistribuicaoTuirFulan"),
    
    path('report/product/production/<str:hashid>/year/<str:hashid1>', views.reportProdusaunTuirTinan, name="reportProdusaunTuirTinan"),
    path('report/product/distribution/<str:hashid>/year/<str:hashid1>', views.reportDistribuicaoTuirTinan, name="reportDistribuicaoTuirTinan"),
    
    # # pedidu
    # path('product-request/list/', views.ProductRequestList, name="product-request-list"),
    # path('dist/request/detail/<str:hashid>', views.DistRequestDetail, name="dist-detallu-pedidu"),
    # path('dist/request/has-delivered/<str:hashid>', views.DistRequestProductDelivered, name="dist-konfirma-entrega-ona-produtu"),
 
]