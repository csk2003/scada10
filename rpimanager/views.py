from django.shortcuts import render
from django.http import HttpResponse
from rpimanager.models import Pole
# Create your views here.

def listallpoles(request):
	polelist = Pole.objects.all().values()
	# context = {'pole_list': polelist}
	# return render(request, 'pole_overview.html', context)
	return polelist

