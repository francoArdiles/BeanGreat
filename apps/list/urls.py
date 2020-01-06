from django.conf.urls import url
from django.urls import path
from . import views

# app_name='lista'
urlpatterns = [
    url(r'^listas/$', views.shopping_carts, name='shopping_carts'),
    path(r'lista/<int:pk>', views.shopping_cart, name='shopping_cart'),
]

