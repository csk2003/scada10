from django.shortcuts import render
from django.http import HttpResponse
from rpimanager.models import Pole
import json
# Create your views here.

def listallpoles(request):
	polelist = Pole.objects.all().values()
	# context = {'pole_list': polelist}
	# return render(request, 'pole_overview.html', context)
	dump = json.dumps(polelist)
    return HttpResponse(dump, content_type='application/json')

