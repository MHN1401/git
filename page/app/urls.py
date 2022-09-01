from django.urls import path

from . import views

urlpatterns = [
    path('' , views.mainpage, name='mainpage'),
    path('<int:ID>', views.detail, name='detail'),
    path('go/<name>', views.go, name='go'),
    path('hello/', views.hello, name='hello'), 
    path('inc/', views.inc, name='inc'), 
    path('salam/<name>', views.salam, name='salam'),
    path('test/', views.test, name='test'),
]
