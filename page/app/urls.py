from django.urls import path

from . import views

urlpatterns = [
    path('go/<name>', views.go, name='go'),
    path('hello/', views.hello, name='hello'), 
    path('inc/', views.inc, name='inc'), 
    path('salam/<name>', views.salam, name='salam'),
    path('test/', views.test, name='test'),
]

