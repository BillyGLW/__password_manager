from django.urls import reverse

from django.http import HttpResponse
from django.http import HttpResponseRedirect

def rrol(request):
	# HttpResponseRedirect.status_code = 404
	return HttpResponseRedirect('https://youtu.be/oHg5SJYRHA0?t=1')
