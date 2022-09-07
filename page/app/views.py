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
from .models import Work, Employee


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
    page_number = request.GET.get('page', request.session.get('page' , 1))
    request.session['page'] = page_number
    page_obj = paginator.get_page(page_number)
    context = {'work' : work , 'page_obj' : page_obj , 'num_visit' : num_visit}
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
            if user is not None:
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
def new_work(request):
    return render(request, 'html/new_work.html')
