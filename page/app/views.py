from django.http import HttpResponse  
from django.shortcuts import render, redirect, get_object_or_404  
from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate, logout  
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User  
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from django.core.mail import EmailMessage  
from django.core.paginator import Paginator
from .tokens import account_activation_token  
from .forms import SignupForm  
from .models import Work, Employee, Karfarma, Karmand
from django.utils import timezone


def user_required(Type):
    def decorator(func):
        def inner(request, *args, **kwargs):        
            user = request.user
            if hasattr(user,'%s'%Type):
                return func(request, *args, **kwargs)
            return HttpResponse("<center><h1>you are not %s</h1></center>"%Type)
        return inner
    return decorator

def hello(request):
    return HttpResponse("<h1 style='text-align:center;'>Hello World</h1>")

@login_required
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
    number_of_page = paginator.num_pages
    page_number = request.GET.get('page', request.session.get('page' , 1))
    request.session['page'] = page_number
    page_obj = paginator.get_page(page_number)
    context = {'work' : work , 'page_obj' : page_obj , 'num_visit' : num_visit, 'page_number' : number_of_page}
    return render(request, 'html/index.html', context)

def detail(request,ID):
    work = get_object_or_404(Work, pk=ID)
    context = {'work' : work}
    return render(request, 'html/detail.html', context)

def signup(request):  
    if request.method == 'POST':  
        form = SignupForm(request.POST)  
        if form.is_valid():  
            user = form.save()  
            user.is_active = False  
            if request.POST.get('karfarma') :
                user.karfarma = Karfarma(user = user).save()
            else:
                user.karmand = Karmand(user = user).save()
            user.save()  
            # to get the domain of the current site  
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('html/acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  
            return HttpResponse('Please confirm your email address to complete the registration')  
    else:  
        form = SignupForm()  
    return render(request, 'html/signup.html', {'form': form}) 

def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!')  

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("mainpage")
def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('mainpage')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.") 
    form = AuthenticationForm()
    return render(request = request,
                  template_name = "html/login.html",
                  context={"form":form})

@user_required("karfarma")
def new_work(request):
    if request.method == 'POST' :
        user = request.user
        x = request.POST
        w = Work(work_title = x['title'], price = x['price'], time = x['time'], employer = user.username, info = x['info'], pub_date = timezone.now())
        w.save()
        return redirect('mainpage')
    return render(request, 'html/new_work.html')

@user_required("karmand")
def assign_work(request,ID):
    user = request.user.karmand
    work = Work.objects.get(id=ID)
    work.karmand = user
    work.save()
    return redirect('detail', ID)

@user_required("karmand")
def unassign_work(request,ID):
    work = Work.objects.get(id=ID)
    work.karmand = None
    work.save()
    return redirect('detail', ID)

@login_required
def delete_work(request,ID):
    work = Work.objects.get(id=ID)
    if request.user.is_superuser or work.employer == request.user.username:       
        work.delete()
        return redirect('mainpage')
    return HttpResponse("you dont have permission to do this")

import json
def json_work(request, objects):
    data = list()
    for i in objects:
        can_del = True if (request.user.is_superuser or request.user.username == i.employer) else False
        data.append({'work_title': i.work_title, 
                     'price': i.price,
                     'time': i.time,
                     'employer': i.employer,
                     'id': i.id,
                     'can_del': can_del,
                    })
    return data

def load_more(request, page_number):
    work = Work.objects.all().order_by('pub_date')
    paginator = Paginator(work,10)
    data = list()
    if request.GET.get('all'):
        while page_number <= paginator.num_pages:
            data += json_work(request, paginator.page(page_number))
            page_number+= 1
    else:
        page_obj = paginator.page(page_number)
        data += json_work(request, page_obj)
    return HttpResponse(json.dumps(data), content_type="application/json")
