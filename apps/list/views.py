from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ShoppingCart
from django.views.decorators.csrf import csrf_exempt
from apps.codes import models as codes
from django.http import JsonResponse
from .forms import ShoppingCartForm


@login_required
def shopping_carts(request):
    user = request.user
    context = {'form': ShoppingCartForm(),
               'shopping_carts': user.shoppingcart_set.all()}
    # Debe mostrar la listas de inventarios registrados para el usuario
    return render(request, 'shopping_cart/index.html', context)


@login_required
def shopping_cart(request, pk):
    context = {}
    current_list = request.user.shoppingcart_set.get(id=int(pk))
    if current_list is not None:
        context['list'] = current_list
        context['products'] = current_list.shoppingproduct_set.all()
    else:
        return shopping_carts(request)
    return render(request, 'shopping_cart/shopping_cart.html', context)


def create_shopping_cart(request):
    print('creating inventory')
    if request.method == 'POST':
        name = request.POST.get('create_data')

        new_shopping_cart = ShoppingCart(name=name, owner=request.user)
        new_shopping_cart.save()
        new_shopping_cart.users.add(request.user)
        new_shopping_cart.save()

        response_data = {
            'result': 'Lista de compras creada!',
            'inventory_pk': new_shopping_cart.pk,
            'name': new_shopping_cart.name,
            'abs_url': new_shopping_cart.get_absolute_url(),
            'count_items': '0',
            'count_user': '1',
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'Vacio': 'Aquí no hay nada'})


@csrf_exempt
def delete_shopping_cart(request):
    if request.method == 'POST':
        pk = request.POST.get('element_pk')
        ShoppingCart.objects.get(id=pk).delete()
        return JsonResponse({'url': '/listas/'})
    else:
        return JsonResponse({'Vacio': 'Aqui no hay nada'})


@csrf_exempt
def share_shopping_cart_code(request):
    if request.method == 'POST':
        pk = request.POST.get('element_pk')
        current_shopping_cart = ShoppingCart.objects.get(id=pk)
        if len(current_shopping_cart.codeshoppingcart_set.all())>0:
            pass
        code = codes.CodeShoppingCart(shopping_cart=current_shopping_cart)
        code.save(id_object=pk)
        return JsonResponse({'code': code.code})
    return JsonResponse({'Vacio': 'Aqui no hay nada'})


@csrf_exempt
def join_shopping_cart(request):
    if request.method == 'POST':
        code = request.POST.get('join_data')
        print(code)
        code_object = codes.CodeShoppingCart.objects.get(code=code)
        if code_object.is_outdated():
            code_object.delete()
            return JsonResponse({'outdated': 'Codigo caducado'})
        code_object.shopping_cart.users.add(request.user)
        return JsonResponse({'url': code_object.shopping_cart.get_absolute_url()})
    else:
        return JsonResponse({'Vacio': 'Aqui no hay nada'})
