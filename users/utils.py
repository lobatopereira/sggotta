from client.models import ClientUser

def c_user_client(user):
	objects = ClientUser.objects.filter(user=user).first()
	client = ""
	if objects:
		client = objects.client
	return client