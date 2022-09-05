from django.shortcuts import render , redirect

# Create your views here.
from django.http import HttpResponse
from .models import Work
from django.core.paginator import Paginator

def hello(request):
    return HttpResponse("<h1 style='text-align:center;'>Hello World</h1>")

def salam(request,name):
 return HttpResponse("<h1 style='text-align:center;'>salam {}</h1>".format(name))

x=0
def inc(request):
    global x
    x+=1
    return HttpResponse("<h1 style='text-align:center;'>number of refresh : {} </h1>".format(x) )

def go(request,name):
    return redirect("https://google.com/search?q={}".format(name))

def test(request):
    return HttpResponse("<h1 style='text-align:center'> This is for test</h1>")

def mainpage(request):
    num_visit = request.session.get('num_visit' , 0)
    request.session['num_visit'] = num_visit + 1

    work = Work.objects.all()
    paginator = Paginator(work, 10)
    page_number = request.GET.get('page', request.session.get('page' , 1))
    request.session['page'] = page_number
    page_obj = paginator.get_page(page_number)
    context = {'work' : work , 'page_obj' : page_obj , 'num_visit' : num_visit}
    return render(request, 'html/index.html', context)

def detail(request,ID):
    work = Work.objects.get(id=ID)
    context = {'work' : work}
    return render(request, 'html/detail.html', context)
