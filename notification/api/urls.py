from django.urls import path
from . import views

urlpatterns = [
    path('badge/distribution/request/', views.APINotifBadgeDist.as_view()),
    path('pedidu/distribution/foun/', views.APINotifPediduFoun.as_view()),
    # path('implementation/dir/mun/', views.APINotifImplementasaunDirMun.as_view()),
    
    # # adminpostu
    # path('badge/funsionariu/postu/', views.APINotifBadgeFunPost.as_view()),
    # path('survey/rejeitadu/funsionariu/postu/', views.APINotifSurveyRejeitaduFunPost.as_view()),
    # path('implementasaun/rejeitadu/funsionariu/postu/', views.APINotifImplementasaunRejeitaduFunPost.as_view()),
 
]