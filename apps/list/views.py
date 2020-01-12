from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ShoppingCart, ShoppingProduct
from django.views.decorators.csrf import csrf_exempt
from apps.codes import models as codes
from django.http import JsonResponse
from django.urls import reverse
from .forms import ShoppingCartForm, ShoppingProductForm
from .. import utils


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
    codes = current_list.codeshoppingcart_set.all() or None
    if current_list is not None:
        context['shopping_cart'] = current_list
        context['items'] = current_list.shoppingproduct_set.all()
        context['product_form'] = ShoppingProductForm(initial={'quantity': 1})
        context['url_add'] = reverse('add_shoppping_cart_product')
        context['url_delete_product'] = reverse('delete_shopping_cart_product')
        context['url_delete_this'] = reverse('delete_shopping_cart')
        context['url_fill_shopping_cart'] = reverse('fill_from_container')
        # context['shopping_carts'] = request.user.shoppingcart_set.all()
        if codes is not None:
            for _code in codes:
                if _code.is_outdated():
                    print('{} is outdated'.format(_code.code))
                    _code.delete()
        context['codes'] = codes
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
        return JsonResponse({'url': reverse('shopping_carts'),
                             'action': 'redirect'})
    else:
        return JsonResponse({'Vacio': 'Aqui no hay nada'})


@csrf_exempt
def share_shopping_cart_code(request):
    if request.method == 'POST':
        pk = request.POST.get('element_pk')
        current_shopping_cart = ShoppingCart.objects.get(id=pk)
        if len(current_shopping_cart.codeshoppingcart_set.all()) > 0:
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
        return JsonResponse(
            {'url': code_object.shopping_cart.get_absolute_url()})
    else:
        return JsonResponse({'Vacio': 'Aqui no hay nada'})


def add_product(request):
    print('adding product inventory')
    print(request)
    print(request.POST)
    response_data = {}
    if request.method == 'POST':
        id_sh_cart = request.POST.get('pk_container')
        # Carga formulario al objeto
        data = utils.deserialize_form(request.POST.get('data'))
        # product = _add_product(data, id_sh_cart)
        form = ShoppingProductForm(data)
        if form.is_valid():
            product = form.save(container_id=id_sh_cart)
            print(product)
            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': form.errors})
    else:
        return JsonResponse({'Vacio': 'Aquí no hay nada'})


@csrf_exempt
def delete_product(request):
    print('eliminando producto')
    # FIXME: implementar
    return JsonResponse({'Vacio': 'Aquí no hay nada'})
    pass


def fill_from_container(request):
    # revisar
    # layout/templates/shopping/create_from_ivnentory.html
    # layout/static/js/shopping_cart/create_shoppiing_cart_from_container.js
    #
    # Idealmente usariamos esta view para crear la lista a partir de otra
    # losta y a partir de una despensa
    print('en view fill_from_container')
    if request.method == 'POST':
        data = utils.deserialize_form(request.POST.get('data'))
        products = data['item-shopping-cart']
        name = data['shopping-cart-name']
        shopping_cart_id = data['shopping-cart-id']
        # Si no existe, entonces se crea una nueva lista de compras
        if shopping_cart_id == 'new':
            current_shopping_cart = ShoppingCart(name=name, owner=request.user)
            current_shopping_cart.save()
            current_shopping_cart.users.add(request.user)
            shopping_cart_id = current_shopping_cart.pk
        else:
            current_shopping_cart = ShoppingCart.objects.get(
                pk=shopping_cart_id)
        # Crear nuevos productos en la lista
        if isinstance(products, list):
            for item in products:
                print('item creado', item)
                product = ShoppingProduct(product_id=item,
                                          list_id=shopping_cart_id)
                product.save()
        else:
            product = ShoppingProduct(product_id=products,
                                      list_id=shopping_cart_id)
            product.save()

        from pprint import pprint
        pprint(data)
    return JsonResponse({})
