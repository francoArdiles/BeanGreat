from django.shortcuts import render
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
