from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login as login_user


def login(request):
	state = "Please log in below..."
	username = password = ''
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login_user(request, user)
				state = "You're successfully logged in!"
			else:
				state = "Your account is not active, please contact the site admin."
		else:
				state = "Your username and/or password were incorrect."

	return render_to_response('login.html', {'state': state, 'username': username})
