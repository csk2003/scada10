from django.shortcuts import render
from django.http import HttpResponse
from scada10.rpimanager import models
# Create your views here.

def listallpoles(request):
	'''
	polelist = Pole.objects.all()
	context = {'pole_list': polelist}
	return render(request, 'pole_overview.html', context)

	'''
	return HttpResponse('<h1>POLE list section</h1>')

