from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
# Create your views here.
from rest_framework import viewsets, request

from .serializers import *
from .models import *


class GeoNoteViewSet(viewsets.ModelViewSet):
    queryset = GeoNote.objects.all().order_by('user')
    serializer_class = GeoNoteSerializer

class StackedImageViewSet(viewsets.ModelViewSet):
    queryset = StackedImage.objects.all().order_by('user')
    serializer_class = StackedImageSerializer

class OverlayImageViewSet(viewsets.ModelViewSet):
    queryset = OverlayImage.objects.all().order_by('user')
    serializer_class = StackedImageSerializer

def request_overlay(httprequest: request):
    if httprequest.method == 'GET':
        reqdata = httprequest.data
        
    else:
        #TODO: give an error
        return False

