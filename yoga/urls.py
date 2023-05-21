from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import views




app_name = 'yoga'


urlpatterns =[
    path('',views.index,name ='index'),
    path('sss/',views.sss,name='sss',),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('list/',views.blog_list,name='list'),
    path('<str:slug>/',views.blog_detail,name='blog_detail'),

]


