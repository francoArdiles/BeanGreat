from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import InventoryForm
from .models import Inventory
from apps.codes import models as codes


@login_required
def inventories(request):
    user = request.user
    context = {'form': InventoryForm(),
               'inventories': user.inventory_set.all()}
    # Debe mostrar la listas de inventarios registrados para el usuario
    return render(request, 'inventory/index.html', context)


@login_required
def inventory(request, pk):
    context = {}
    current_inventory = Inventory.objects.get(id=int(pk))
    codes = current_inventory.codeinventory_set.all() or None

    if request.user in current_inventory.users.all():
        context['inventory'] = current_inventory
        context['items'] = current_inventory.inventoryproduct_set.all()
        # Elimina los codigos que no estan actualizados de la base de datos
        if codes is not None:
            for _code in codes:
                if _code.is_outdated():
                    print('{} is outdated'.format(_code.code))
                    _code.delete()
        context['codes'] = codes
    else:
        return inventories(request)
    return render(request, 'inventory/inventory.html', context)


def create_inventory(request):
    print('creating inventory')
    if request.method == 'POST':
        inventory_name = request.POST.get('inventory_data')

        new_inventory = Inventory(name=inventory_name, owner=request.user)
        new_inventory.save()
        new_inventory.users.add(request.user)
        new_inventory.save()

        response_data = {
            'result': 'Despensa creada!',
            'inventory_pk': new_inventory.pk,
            'name': new_inventory.name,
            'abs_url': new_inventory.get_absolute_url(),
            'count_items': '0',
            'count_user': '1',
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'Vacio': 'Aquí no hay nada'})


@csrf_exempt
def delete_inventory(request):
    if request.method == 'POST':
        pk = request.POST.get('inventory_pk')
        Inventory.objects.get(id=pk).delete()
        return JsonResponse({'url': '/despensas/'})
    else:
        return JsonResponse({'Vacio': 'Aqui no hay nada'})


@csrf_exempt
def share_inventory_code(request):
    if request.method == 'POST':
        pk = request.POST.get('inventory_pk')
        current_inventory = Inventory.objects.get(id=pk)
        if len(current_inventory.codeinventory_set.all())>0:
            pass
        code = codes.CodeInventory(inventory=current_inventory)
        code.save(id_object=pk)
        return JsonResponse({'code': code.code})
    return JsonResponse({'Vacio': 'Aqui no hay nada'})


@csrf_exempt
def join_inventory(request):
    if request.method == 'POST':
        code = request.POST.get('inventory_code')
        code_object = codes.CodeInventory.objects.get(code=code)
        if code_object.is_outdated():
            code_object.delete()
            return JsonResponse({'outdated': 'Codigo caducado'})
        code_object.inventory.users.add(request.user)
        return JsonResponse({'url': code_object.inventory.get_absolute_url()})
    else:
        return JsonResponse({'Vacio': 'Aqui no hay nada'})
