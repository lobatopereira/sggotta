from django.shortcuts import render,redirect, get_object_or_404,HttpResponse
from django.contrib.auth.models import Group,User
from django.contrib.auth.decorators import login_required
from .forms import *
from custom.utils import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from users.models import Profile

from users.decorators import allowed_users

# Create your views here.
@login_required
@allowed_users(allowed_roles=['admin'])
def userlist(request):
	userlist = User.objects.all().exclude(is_staff=True)
	context = {
		"title":"Lista Utilizador",
		"userlist":userlist,
		"active_userlist":"active",
		"page":"userlist",
	}
	return render(request, "userlist.html",context)

@login_required
def RejistuUtilizador(request):
	group = request.user.groups.all()[0].name
	g_list = ['admin','superadmin']
	groups = Group.objects.all().exclude(name__in=g_list)
	if request.method == 'POST':
		userType = request.POST.get("userType")
		firstname = request.POST.get("firstname")
		lastname = request.POST.get("lastname")
		email = request.POST.get("email")
		password = request.POST.get("password")

		password = make_password(password)
		username = split_string(firstname)
		obj2 = User(username=username, password=password,email=email,is_active=False)
		obj2.save()
		# obj3 = Profile.objects.create(user=obj2,firstname=firstname,lastname=lastname,user_created=request.user)
		group_user = Group.objects.get(id=str(userType))
		user = User.objects.get(id=obj2.id)
		user.groups.add(group_user)
		messages.success(request, f'Dadus Utilizador Rejistu ho Susesu!')
		return redirect('konfigurasaun')
	context = {
		'group':group,'groups':groups,
		'title': 'Rejistu Utilizador',
		'legend': 'Rejistu Utilizador',
	}
	return render(request, 'rejistuUtilizador.html', context)

@login_required
def UserProfile(request):
	group = request.user.groups.all()[0].name
	profile = get_object_or_404(Profile, user=request.user)
	context = {
		'group':group,
		'profile':profile,
		'title': 'Profile Utilizador',
		'legend': 'Profile Utilizador',
	}
	return render(request, 'profile.html', context)

@login_required
def KonfirmaPasswordProfile(request):
	if request.method == 'GET':
		page = request.GET.get("page")
		password = request.GET.get("password")
		user = get_object_or_404(User, id=request.user.id)
		profile = get_object_or_404(Profile, user=user)
		password1 = make_password(password)
		print(password1)

		if page == "userProfile":
			authentic = authenticate(username = user.username, password = password)
			if authentic:
				messages.success(request, f'Your Password is Authenticated!')
				return redirect('UpdateProfileUtilizador')
			else:	
				messages.warning(request, f'Your Password is not Authenticated!')
				return redirect('UserProfile')
		elif page == "userPhoto":
			authentic = authenticate(username = user.username, password = password)
			if authentic:
				messages.success(request, f'Your Password is Authenticated!')
				return redirect('UpdateUserProfilePhoto', profile.id)
			else:	
				messages.warning(request, f'Your Password is not Authenticated!')
				return redirect('UserProfile')
	

@login_required
def UpdateProfileUtilizador(request):
	group = request.user.groups.all()[0].name
	profile = get_object_or_404(Profile, user=request.user)
	if request.method == 'POST':
		form = ProfileUpdateForm(request.POST, instance=profile)
		if form.is_valid():
			form.save()
			messages.success(request, f'Your Profile has been updated!')
			return redirect('UserProfile')
	else:
		form = ProfileUpdateForm(instance=profile)

	context = {
		'group':group,
		'form': form,
		'title': 'Update Profile Utilizador',
		'legend': 'Update Profile Utilizador',
	}
	return render(request, 'UpdateProfile.html', context)

@login_required
def UpdateUserProfilePhoto(request,id):
	group = request.user.groups.all()[0].name
	profile = get_object_or_404(Profile, id=id)
	if request.method == 'POST':
		form = PhotoProfileUpdateForm(request.POST,request.FILES, instance=profile)
		
		if form.is_valid():
			form.save()
			messages.success(request, f'Your Profile Photo has been updated!')
			return redirect('UserProfile')
	else:
		form = PhotoProfileUpdateForm(instance=profile)

	context = {
		'group':group,
		'form': form,
		'profile': profile,
		'title': 'Update Photo Profile Utilizador',
		'legend': 'Update Photo Profile Utilizador',
	}
	return render(request, 'UpdateProfile.html', context)

@login_required
def manageAccount(request):
	group = request.user.groups.all()[0].name
	if request.method == 'POST':
		form = UserUpdateForm(request.POST, instance=request.user)
		
		if form.is_valid():
			form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('manageAccount')
	else:
		form = UserUpdateForm(instance=request.user)

	context = {
		'group':group,
		'form': form,
		'title': 'Account Info',
		'legend': 'ACCOUNT INFO',
	}
	return render(request, 'account.html', context)

@login_required
def userProfile(request):
	group = request.user.groups.all()[0].name
	context = {
		'group':group,
		'profile': profile,
		'title': 'Profile Utilizador',
	}
	return render(request, 'profile.html', context)

@login_required
def changeAccountPassword(request):
	group = request.user.groups.all()[0].name
	if request.method == 'POST':
		current_password = request.POST["old_password"]
		new_password = request.POST["new_password"]
		confirm_password = request.POST["confirm_password"]

		user = User.objects.get(id=request.user.id)
		un = user.username
		pwd = new_password
		check = user.check_password(current_password)
		if check==True:
			if new_password == confirm_password:
				user.set_password(new_password)
				user.save()
				authenticate(username = un, password = pwd)
				if request.user.is_authenticated:
					messages.info(request, f'Your password has been changed Successfuly!')
					return redirect('changeAccountPassword')
			else:
				messages.warning(request, f'Your New password {new_password} and Confirmation Password {confirm_password} does not match!')
				return redirect('changeAccountPassword')
		else:
			messages.warning(request, f'Your current password {current_password} is Incorrect!')
			return redirect('changeAccountPassword')

	context = {
		'group':group,
		'title': 'Change Password',
		'legend': 'CHANGE PASSWORD',
	}
	return render(request, 'changeAccountPassword.html', context)

@login_required
@allowed_users(allowed_roles=['admin'])
def resetUserPassword(request,id):
	userData = get_object_or_404(User,id=id)
	password = make_password('password')
	userData.password = password
	userData.save()
	messages.success(request, f'Password ba {userData.username} Reset ho Susesu!')
	return redirect('konfigurasaun')

@login_required
@allowed_users(allowed_roles=['admin'])
def desativuUser(request,id):
	userData = get_object_or_404(User,id=id)
	userData.is_active = False
	userData.save()
	messages.success(request, f'User {userData.username} Desativu ho Susesu!')
	return redirect('konfigurasaun')

@login_required
@allowed_users(allowed_roles=['admin'])
def ativuUser(request,id):
	userData = get_object_or_404(User,id=id)
	userData.is_active = True
	userData.save()
	messages.success(request, f'User {userData.username} Ativu ho Susesu!')
	return redirect('konfigurasaun')

@login_required
@allowed_users(allowed_roles=['admin'])
def deleteUser(request,id):
	user = get_object_or_404(User,id=id)
	user.delete()
	messages.error(request, f'Utilizador ba {user.username} Hamoos ho Susesu!')
	return redirect('konfigurasaun')


def KonfirmaNoManejaPasswordUtilizador(request, hashid):
	userProfile = get_object_or_404(Profile,id=hashid)
	user = User.objects.get(id=userProfile.user.id)
	if request.method == 'POST':
		password1 = request.POST.get("password1")
		password2 = request.POST.get("password2")
		if password1 == password2:
			user.set_password(password1)
			user.is_active = True
			user.save()
			messages.success(request, f'Ita boot Susesu Ativu Konta utilizador. Tuir mai bele Login!')
			return redirect('login')
		else:
			messages.error(request, f'Password no Konfirmasaun Password la Loos!')
			return redirect('KonfirmaNoManejaPasswordUtilizador',userProfile.id)
	context = {
		'user':user,
		'userProfile':userProfile,
		'title': 'Konfirma no Kria Password Utilizador',
	}
	return render(request, 'KonfirmaNoManejaPasswordUtilizador.html', context)