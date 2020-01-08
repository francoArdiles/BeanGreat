from django.conf.urls import url
from django.urls import path, include
from . import views


urlpatterns = [
    url(r'^despensas/$', views.inventories, name='inventories'),
    path(r'despensa/<int:pk>/', views.inventory, name='inventory'),
    url(r'crear-despensa/$', views.create_inventory, name='create_inventory'),
    url(r'eliminar-despensa/$', views.delete_inventory,
         name='delete_inventory'),
    url(r'despensa/unirse-a-despensa/$', views.join_inventory,
        name='join_inventory'),
    url(r'despensa/share-code/$', views.share_inventory_code,
        name='share_inventory'),

]

