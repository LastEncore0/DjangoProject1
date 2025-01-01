from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse, resolve


# Create your views here.
def index(request):
    return  HttpResponse("order")

def list(request, year, month, day):
    # kwargs = {"year": 2025, "month": 10, "day": 1}
    args = (year, month, day)
    # route_url = reverse("order:list", kwargs=kwargs)
    route_url = reverse("order:list", args=args)
    print("reverse反向解析得到的地址:",route_url)
    result = resolve(route_url)
    print("resolve通過路由地址得到的路由信息:", result)
    return  HttpResponse("order list")
