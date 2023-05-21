from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('take/', views.take, name='take'),


    path('payment/', views.payment, name='payment'),
    path('result/', views.result, name='result'),
    path('success/', views.success, name='success'),
    path('failure/', views.fail, name='failure'),
]
