from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    print("request.GET")
    return render(request,'index2.html')
def blog(request, id):
    if id == 0:
        return redirect("/s1/error.html")
    else:
        return HttpResponse("id:" + str(id))
def blog2(request, id, year, month, day):
    return HttpResponse(str(year) + '/' + str(month) + '/' + str(day) + '/'  +"id:" + str(id))
def blog3(request, year, month, day):
    return HttpResponse(str(year) + '/' + str(month) + '/' + str(day))