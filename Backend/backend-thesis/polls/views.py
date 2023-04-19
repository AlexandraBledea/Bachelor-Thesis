from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse


def index(request):
    return JsonResponse({'ana': "Hello world. You're at the polls index."})
