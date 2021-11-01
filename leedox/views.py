from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse("환영합니다, Hello, Welcome to LEEDOX!")