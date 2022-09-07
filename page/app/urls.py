from django.urls import path,include

from . import views

urlpatterns = [
    path('' , views.mainpage, name='mainpage'),
    path('<int:ID>', views.detail, name='detail'),
    path('go/<name>', views.go, name='go'),
    path('hello/', views.hello, name='hello'), 
    path('inc/', views.inc, name='inc'), 
    path('salam/<name>', views.salam, name='salam'),
    path('test/', views.test, name='test'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate'),
    path('new_work/', views.new_work, name='new_work'),
]
