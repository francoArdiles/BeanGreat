from django.conf.urls import url
from django.urls import path
from . import views

# app_name='lista'
urlpatterns = [
    url(r'^listas/$', views.shopping_carts, name='shopping_carts'),
    path(r'lista/<int:pk>', views.shopping_cart, name='shopping_cart'),
    url(r'crear-lista/$', views.create_shopping_cart, name='create_shopping_cart'),
    url(r'eliminar-lista/$', views.delete_shopping_cart,
         name='delete_shopping_cart'),
    url(r'despensa/unirse-a-lista/$', views.join_shopping_cart,
        name='join_shopping_cart'),
    url(r'lista/share-code/$', views.share_shopping_cart_code,
        name='share_shopping_cart'),
    url(r'shopping_cart/delete_product/$', views.delete_product,
        name='delete_shopping_cart_product'),
    url(r'shopping_cart/add_product/$', views.add_product,
        name='add_shoppping_cart_product')

]

