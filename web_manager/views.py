import os
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.shortcuts import render
from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import web_manager_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_exempt
import scrypt, base64
import pickle, hashlib, zlib
import urllib.request, urllib.parse, urllib.error

import sys
import json
import datetime
from django.utils.timezone import utc

# Temporary link settings
hash_secret = "wojciechnowak"
# Time that link is valid in minutes
link_time_period = 5


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
        # 'Content-Length: {content_length}\n'
        # 'Content-Type: {content_type}\n'
        '{headers}\n\n'
        '{body}'
    ).format(
        method=request.method,
        # content_length=request.META['CONTENT_LENGTH'],  not existing? why?
        # content_type=request.META['CONTENT_TYPE'], # same ?
        headers=headers,
        body=request.body,
    )

# Ned Batchelder: https://stackoverflow.com/questions/1360101/how-to-generate-temporary-urls-in-django
def encode_data(data):
    """Turn `data` into a hash and an encoded string, suitable for use with `decode_data`."""
    compressed_text = zlib.compress(pickle.dumps(data, 0))
    text = base64.b64encode(compressed_text).decode().replace('\n', '')
    m = hashlib.md5(str.encode('{}{}'.format(hash_secret, text))).hexdigest()[:12]
    return m, text

def decode_data(hash, enc):
    """The inverse of `encode_data`."""
    text = urllib.parse.unquote(enc)
    m = hashlib.md5(str.encode('{}{}'.format(hash_secret, text))).hexdigest()[:12]
    if m != hash:
        raise Exception("Bad hash!")
    data = pickle.loads(zlib.decompress(base64.b64decode(text)))
    return data

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
		return HttpResponseRedirect(reverse_lazy("web_manager:index"))
	except:
		return HttpResponseRedirect(reverse_lazy("web_manager:index"))


def index(request):
	'''
	Main password manager layout with harcoded test user.
	TODO: Extend registration functionality.
	'''
	while 1:
		print(sys.argv)
	try:
		User.objects.get(username='test')
	except User.DoesNotExist:
		user = User.objects.create_user('test', 'test@gmail.com', 'test123', is_staff=True)

	context = {'username': str(request.user), 'request': request, 'pretty_request': pretty_request(request) }
	response = render(request, "frontend-landing_page.html", context)
	return response

def login_user(request):
	'''
	Log in user, then if credentials are ok reverse_lazy to the profile view,
	other way return to index page.
	'''
	username = request.POST['Username']
	password = request.POST['Password']
	user = authenticate(request, username=username, password=password) 
	if user is not None or 'AnonymousUser':
		login(request, user)
		return HttpResponseRedirect(reverse_lazy("web_manager:manage_password", kwargs={'username':user}))
	else:
		return HttpResponseRedirect(reverse_lazy("web_manager:index"))
	context = {'request': pretty_request(request), 'user': str(user) }
	response = render(request, "frontend-landing_page.html", context)
	return response
@csrf_exempt
def wm_shared_password_handle(request, username):
	'''
	Changes password for shared link PM.
	'''
	return HttpResponse(password_manager_update_password(request.POST.dict()))

@csrf_exempt
def wm_password_update(request, username):
	'''
	Changes password for user PM.
	'''
	return HttpResponse(password_manager_update_password(request.POST.dict()))

def password_manager_update_password(obj):
	'''
	requires: password_manager model
	description: changes password based of given dict, handles only single query for given id and password.
	'''
	new_password_str = ''	
	try:
		for x in obj:
			new_password_str += obj[x]
		password_manager = web_manager_password.objects.filter(pk=obj['id']).update(account_password=encrypt_password(new_password_str))
		_request_data = json.dumps({'status': True})
	except:
		_request_data = json.dumps({'status': False})
	return (_request_data)


@csrf_exempt
def shared_link_update(request, username, hash, enc):
	'''
	Link with hashed stored in the URI.
	'''
	decode = decode_data(hash, str(enc))
	if (decode[1] < datetime.datetime.now() + datetime.timedelta(minutes=link_time_period)) 
	and (decode[1] > datetime.datetime.now() - datetime.timedelta(minutes=link_time_period)):
		arguments = list(str(decode[0]).split(','))
		password_manager = web_manager_password.objects.filter(id__in=arguments, account_name=username)
		context = {'request': pretty_request(request), 'username': username, 'hash': str(hash), 'enc': enc, 'acc_name': password_manager, 'user_url': ''.join([request.build_absolute_uri()])}
		response = render(request, "frontend-shared-link.html", context)
		return response
	return HttpResponseRedirect(reverse_lazy('web_manager:index'))

def shared_link(request, username):
	'''
	Shared link: making a temporary hash (using secret variable for hashing) 
	based link valid only for 5 minutes.
	'''
	password_manager = web_manager_password.objects.all().filter(account_name=username)
	context = {'request': pretty_request(request), 'username':
				 username, 'acc_name': password_manager,
				 'hash': '849e77ae1b3ceJzTyCkw5ApW90jNyclX5yow4koMVnfPz09JqkwFco25EvUAqXwJnA==(example)'}
	response = render(request, "frontend-share_link.html", context)
	return response

@csrf_exempt
def wm_shared_link_generate(request, username):
	'''
	Making decoded hash consist of selected primary keys, 
	and create date time (to match 5 min valid link).
	'''
	_post_data = request.POST.dict()
	if not (_post_data):
		return HttpResponseRedirect(reverse_lazy('web_manager:shared_link', kwargs={'username': request.user}))
	now = datetime.datetime.now()
	pk = ','.join(_post_data)
	hash, enc = encode_data([pk, now])
	url = json.dumps({'url': reverse('web_manager:shared_link_update', kwargs={'username': username, 'hash': hash, 'enc': enc})})
	return HttpResponse(url)

@csrf_exempt
def wm_delete(request, username):
	'''
	Password Manager: store new user password in db
	'''
	_post_data = request.POST.dict()
	for query in _post_data:
		password_manager = web_manager_password.objects.filter(pk=str(query)).delete()
	return HttpResponse([x for x in _post_data])
	try:
		username = str(username)
		full_url = ''.join([request.build_absolute_uri()])
		_get_user = web_manager_password.objects.create(site_url=full_url, account_name=str(username), account_password=encrypt_password(request.POST['fld_n_password']))
		return HttpResponseRedirect(reverse_lazy("web_manager:manage_password", kwargs={'username':username}))
	except:
		return HttpResponseRedirect(reverse_lazy("web_manager:manage_password", username))

@login_required
def wm_update(request, username):
	'''
	Password Manager: store new user password in db
	'''
	try:
		username = str(username)
		full_url = ''.join([request.build_absolute_uri()])
		_get_user = web_manager_password.objects.create(site_url=full_url, account_name=str(username), account_password=encrypt_password(request.POST['fld_n_password']))
		return HttpResponseRedirect(reverse_lazy("web_manager:manage_password", kwargs={'username':username}))
	except:
		return HttpResponseRedirect(reverse_lazy("web_manager:manage_password", username))

@csrf_exempt
@login_required
def manage_password(request, username):
	if not (str(request.user) == str(username)):
		return HttpResponseRedirect(reverse_lazy('web_manager:manage_password', kwargs={'username': request.user}))
	password_manager = web_manager_password.objects.all().filter(account_name=username)
	# if needed to decode encrypted password, 
	# get value from django QuerySet: password_manager.values('account_password')

	context = {'request': pretty_request(request), 'user': str(request.user), 'acc_name': password_manager }
	response = render(request, "frontend-profile_page.html", context)
	return response
