import os
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import web_manager_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
import scrypt, base64

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#  Pretty Request: https://gist.github.com/defrex/6140951
def pretty_request(request):
    headers = ''
    for header, value in request.META.items():
        if not header.startswith('HTTP'):
            continue
        header = '-'.join([h.capitalize() for h in header[5:].lower().split('_')])
        headers += '{}: {}\n'.format(header, value)

    return (
        '{method} HTTP/1.1\n'
        'Content-Length: {content_length}\n'
        'Content-Type: {content_type}\n'
        '{headers}\n\n'
        '{body}'
    ).format(
        method=request.method,
        content_length=request.META['CONTENT_LENGTH'],
        content_type=request.META['CONTENT_TYPE'],
        headers=headers,
        body=request.body,
    )
def store_new_password(request, username):
	return HttpResponse("heee " + username)
def encrypt_password(user_password):
	decoded_password = base64.b64encode(scrypt.encrypt(user_password, "@!F%$sDaD5*Za!#"))
	return decoded_password
def decrypt_password(user_password):
	decrypted_password = scrypt.decrypt(base64.b64decode(user_password), "@!F%$sDaD5*Za!#")
	return decrypted_password
def wm_logout(request):
	''' 
	User logout 
	'''	
	try:
		logout(request)
		return HttpResponseRedirect(reverse("web_manager:index"))
	except:
		return HttpResponseRedirect(reverse("web_manager:index"))


def index(request):
	'''
	Main password manager layout with harcoded test user.
	TODO: Extend registration functionality.
	'''
	try:
		User.objects.get(username='test')
	except User.DoesNotExist:
		user = User.objects.create_user('test', 'test@gmail.com', 'test123', is_staff=True)

	context = {'username': str(request.user), 'request': request, 'pretty_request': pretty_request(request) }
	response = render(request, "frontend-landing_page.html", context)
	return response

def login_user(request):
	'''
	Log in user, then if credentials are ok reverse to the profile view,
	other way return to index page.
	'''
	username = request.POST['Username']
	password = request.POST['Password']
	user = authenticate(request, username=username, password=password) 
	if user is not None or 'AnonymousUser':
		login(request, user)
		return HttpResponseRedirect(reverse("web_manager:manage_password", kwargs={'username':user}))
	else:
		return HttpResponseRedirect(reverse("web_manager:index"))
	context = {'request': pretty_request(request), 'user': str(user) }
	response = render(request, "frontend-landing_page.html", context)
	return response


def wm_update(request, username):
	'''
	Password Manager: store new user password in db
	'''
	# user = User.objects.create_user('test', 'test@gmail.com', 'test123', is_staff=True)
	# <input name="fld_n_password" id="fld_n_password">
	try:
		# request = None
		full_url = ''.join(['http://', get_current_site(request).domain, obj.get_absolute_url()])
		_get_user = web_manager_password.objects.create(site_url=full_url, account_name=username, account_password=encrypt_password(request.POST['fld_n_password']))
		_get_user = web_manager_password.objects.get(account_name=username)
		return HttpResponseRedirect(reverse("web_manager:manage_password", username))
	except:
		return HttpResponseRedirect(reverse("web_manager:manage_password", username))

@login_required
def manage_password(request, username):
	if not (str(request.user) == str(username)):
		return HttpResponseRedirect(reverse('web_manager:manage_password', kwargs={'username': request.user}))
	password_manager = web_manager_password.objects.all()

	context = {'request': pretty_request(request), 'user': str(request.user), 'acc_name': password_manager }
	response = render(request, "frontend-profile_page.html", context)
	return response
