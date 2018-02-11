from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rpimanager.models import Pole
from django.core import serializers
import json
# Create your views here.

def listallpoles(request):
    polelist = Pole.objects.all()
    # context = {'pole_list': polelist}
    # return render(request, 'pole_overview.html', context)
    dump = serializers.serialize('json', polelist)

    return Response(dump, status=200)

