from django.shortcuts import render, redirect
from apps.layout.views import index
from django.contrib.auth.decorators import login_required
from . import forms
from .models import RecipeItem, RecipeStep


def recipe_book_registered(request):
    return render(request, 'recipe_book/index.html', {})


def recipe_book(request):
    context = {}
    if request.user.is_authenticated:
        return recipe_book_registered(request)
    return render(request, 'recipe_book/index.html', context)


def recipe(request):
    context = {}

    # Las cosas de la receta
    if request.user.is_authenticated:
        return render(request, 'recipe_book/index.html', context)
    return index(request)


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
def favorite_recipes(request):
    context = {}
    return render(request, 'recipe_book/personal/favorites.html', context)


@login_required()
def our_recipes(request):
    context = {}
    if request.user.is_authenticated:
        return render(request, 'recipe_book/personal/my_recipes.html', context)
    return index(request)
