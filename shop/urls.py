from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path('list/', views.product_list, name='product_list'),
    path('<int:id>/<str:slug>/', views.product_detail, name = 'product_detail'),
    path('<str:category_slug>/', views.Show, name='product_list_by_show'),

]