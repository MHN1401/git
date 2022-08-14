from django.shortcuts import render , redirect

# Create your views here.
from django.http import HttpResponse

def hello(request):
    return HttpResponse("<h1 style='text-align:center;'>Hello World</h1>")

def salam(request,name):
 return HttpResponse("<h1 style='text-align:center;'>salam {}</h1>".format(name))

x=0
def inc(request):
    global x
    x+=1
    txt = "<h1 style='text-align:center;'>number of refresh : " + str(x) + "</h1>"
    return HttpResponse(txt)

def Go(request,name):
    return redirect("https://google.com/search?q={}".format(name))

def test(request):
    return HttpResponse("<h1 style='text-align:center'> This is for test</h1>")

def mainpage(request):
    return render(request ,'index.html')
