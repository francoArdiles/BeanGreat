from django.conf.urls import url
from django.urls import path, include
from . import views


urlpatterns = [
    url(r'^despensas/$', views.inventories, name='inventories'),
    path(r'despensa/<int:pk>/', views.inventory, name='inventory'),
]
