from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    return  HttpResponse("user messeage")

def list(request):
    return  HttpResponse("user list")