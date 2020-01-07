from django.shortcuts import render, redirect
from apps.layout.views import index
from django.contrib.auth.decorators import login_required
from . import forms
from .models import RecipeItem, RecipeStep, Recipe


def recipe_book_registered(request):
    return render(request, 'recipe_book/index.html', {})


def recipe_book(request):
    context = {}
    if request.user.is_authenticated:
        return recipe_book_registered(request)
    all_recipes = Recipe.objects.all()
    context['recipes'] = all_recipes
    return render(request, 'recipe_book/index.html', context)


# suena correcto
# yep. esa sería una pagina diferente con un formulario o un boton de
# publicar/rechazar


def recipe(request, pk):
    context = {}
    current_recipe = Recipe.objects.get(id=int(pk))
    items = RecipeItem.objects.filter(recipe=current_recipe)
    context['recipe'] = current_recipe
    context['items'] = items
    pass


@login_required
def create_recipe(request):
    if request.method == 'POST':
        from pprint import pprint
        pprint(request.POST)
        recipe_form = forms.RecipeForm(request.POST)
        items_formset = forms.RecipeItemFormSet(request.POST, prefix='items_formset')
        steps_formset = forms.RecipeStepFormSet(request.POST, prefix='steps_formset')
        if recipe_form.is_valid() and steps_formset.is_valid():
            recipe_ele = recipe_form.save()
            counter = 1
            for form in steps_formset:
                step = form.save(commit=False)
                step.step_order = counter
                step.recipe = recipe_ele
                step.save()
                counter += 1
            return redirect('recipe_book/index.html')
    else:
        recipe_form = forms.RecipeForm(request.GET or None)
        steps_formset = forms.RecipeStepFormSet(
            queryset=RecipeStep.objects.none(), prefix='steps_formset')
        items_formset = forms.RecipeItemFormSet(
            queryset=RecipeItem.objects.none(), prefix='items_formset')
        context = {
            'recipe_form': recipe_form,
            'steps_formset': steps_formset,
            'items_formset': items_formset,
        }
        return render(request, 'recipe_book/personal/create_recipe.html', context)


@login_required()
def review_recipes(request):
    context = {}
    recipes = Recipe.objects.filter(review=True, public=False)
    context['recipes'] = recipes
    return render(request, 'recipe_book/index.html', )


@login_required()
def favorite_recipes(request):
    context = {}
    fav_recipes = request.user.favoriterecipe_set.all()
    context['recipes'] = fav_recipes
    return render(request, 'recipe_book/personal/favorites.html', context)


@login_required()
def our_recipes(request):
    context = {}
    if request.user.is_authenticated:
        personal_recipes = request.user.recipe_set.all()
        context['recipes'] = personal_recipes
        return render(request, 'recipe_book/personal/my_recipes.html', context)
    return index(request)
