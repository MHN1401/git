from django.urls import path,include
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    path('list/', views.list, name='list'),
    path('add/<name>/<number>', views.add, name='add'),
    path('delete/<number>', views.delete, name='delete'),
    path('find/<name>', views.find, name='find'),
    path('' , views.mainpage, name='mainpage'),
    path('<int:ID>', cache_page(20)(views.detail), name='detail'),
#    path('<int:ID>', views.detail, name='detail'),
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
    path('assign_work/<ID>', views.assign_work, name='assign_work'),
    path('unassign_work/<ID>', views.unassign_work, name='unassign_work'),
    path('delete_work/<int:ID>', views.delete_work, name='delete_work'),
    path('load_more/<int:page_number>', views.load_more, name='load_more'),
]
