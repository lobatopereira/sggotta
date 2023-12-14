from django.urls import path
from . import views
urlpatterns = [
	# path('userlist/',views.userlist, name="userlist"),
	path('Rejistu/Utilizador/',views.RejistuUtilizador, name="RejistuUtilizador"),
	path('Profile/Utilizador/',views.UserProfile, name="UserProfile"),
	path('Update/Profile/Utilizador/',views.UpdateProfileUtilizador, name="UpdateProfileUtilizador"),
	path('Update/Photo/Profile/Utilizador/<str:id>',views.UpdateUserProfilePhoto, name="UpdateUserProfilePhoto"),
	path('Update/Profile/Utilizador/',views.UpdateProfileUtilizador, name="UpdateProfileUtilizador"),
	
	path('Konfirma/Password/Utilizador/',views.KonfirmaPasswordProfile, name="KonfirmaPasswordProfile"),
	
	
	path('manage-user-account/', views.manageAccount, name="manageAccount"),
	path('view-user-profile/', views.userProfile, name="userProfile"),
	path('change-user-password/', views.changeAccountPassword, name="changeAccountPassword"),

	path('reset-user-password/<str:id>', views.resetUserPassword, name="resetUserPassword"),
	path('delete-user/<str:id>', views.deleteUser, name="deleteUser"),
	path('ativu-user/<str:id>', views.ativuUser, name="ativuUser"),
	path('desativu-user/<str:id>', views.desativuUser, name="desativuUser"),

	path('konfirma-no-maneja-utilizador/<str:hashid>',views.KonfirmaNoManejaPasswordUtilizador, name="KonfirmaNoManejaPasswordUtilizador"),
]