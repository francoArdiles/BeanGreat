from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'recetario/$', views.recipe_book, name='recipe_book'),
    url(r'^recetario/favoritos/$', views.favorite_recipes,
        name='favorite_recipes'),
    url(r'^recetario/mis-recetas/$', views.our_recipes, name='my_recipes'),
    url(r'^recetario/crear-receta/$', views.create_recipe, name='create_recipe'),
]