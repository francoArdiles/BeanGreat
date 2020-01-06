from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import InventoryForm
from .models import Inventory


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
    if request.user in current_inventory.users.all():
        context['inventory'] = current_inventory
        context['items'] = current_inventory.inventoryproduct_set.all()
    else:
        return inventories(request)
    return render(request, 'inventory/inventory.html', context)


def create_inventory(request):
    print('creating inventory')
    if request.method == 'POST':
        inventory_name = request.POST.get('inventory_data')
        response_data = {}

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


def delete_inventory(request):
    id_inventory = ''
    if request.method == 'POST':
        Inventory.objects.get(id=id_inventory).delete()
        redirect('inventories')
    else:
        return JsonResponse({'Vacio': 'Aqui no hay nada'})
