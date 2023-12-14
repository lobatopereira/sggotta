from django.urls import path
from . import views
urlpatterns = [
	path('new-request-from-client/list/',views.NotifListaPediduFoun, name="lista-pedidu-foun-husi-cliente"),
	path('new-request-from-client/detail/<str:hashid>',views.NotifDetalluPediduFoun, name="detallu-pedidu-foun-husi-cliente"),
	
	path('distribution-check-request-item/detail/<str:hashid>',views.DistCheckRequestItem, name="distribution-check-request-item"),
	path('distribution-imprimi-nota-pedidu/detail/<str:hashid>',views.DistPrintRequestItemNote, name="distribution-imprimi-nota-pedidu"),
	path('distribution-distribui-request-produtu/detail/<str:hashid>',views.DistDistribuiitemRequest, name="distribution-distribui-request-produtu"),
	
]