from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.layout.views import index

@login_required
def shopping_carts(request):
    user = request.user
    context = {
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
