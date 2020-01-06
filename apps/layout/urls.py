from django.conf.urls import url
from django.contrib.auth.views import logout_then_login
from django.urls import path, include
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'perfil/$', views.profile, name='profile'),
    url(r'^login/$', views.login, name='login'),
    path(r'', include('apps.recipe_book.urls')),
    path(r'', include('apps.list.urls')),
]


