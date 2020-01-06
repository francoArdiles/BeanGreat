from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from ..accounts import forms as account_forms

from .. import constants, utils as utils
from ..inventory.models import Inventory
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login

from ..codes import models as codes

from django.conf import settings


# Aqui se guardan y actualizan los modelos. Aquellos que requieran otras
# partes, como Propietario deben ser creados aqui
# Los datos generados automaticamente alg uardar los modelos deben ser hechos
# sobreescribiendo el metodo save de dicho modelo (por ejemplo: Inventory)


def login_redirect_me(user, request):
    """
    Inicia la sesion de un usuario. Si viene de una pagina previa, lo redirige
    a esa, en caso contrario lo redirige a sus inventarios

    :param user: usuario registrado
    :param request: request de la pagina entregado por el usuario

    :return: redireccion a nueva url
    """
    do_login(request, user,
             backend='allauth.account.auth_backends.AuthenticationBackend')
    if 'next' in request.POST:
        return redirect(request.POST.get('next'))

    return redirect('index')


def login(request):
    context = {}
    # if user is authenticated can't get in login page
    if request.user.is_authenticated:
        return login_redirect_me(request.user, request)

    if request.method == 'POST':
        # registrarse
        if request.POST.get('submit') == 'sign_up':
            form = account_forms.RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                return login_redirect_me(user, request)
        # inicio de sesion
        elif request.POST.get('submit') == 'sign_in':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                user = authenticate(username=username, password=password)

                if user is not None:
                    return login_redirect_me(user, request)

    context['signUpForm'] = account_forms.RegistrationForm()
    context['signInForm'] = AuthenticationForm()

    return render(request, 'accounts/registration/login.html', context)


@login_required
def index(request):
    # TODO Enviar a pagina estatica si no hay usuario registrado
    context = {}

    return render(request, 'index/index.html', context)


@login_required
def profile(request):
    context = {}
    return render(request, 'accounts/profile/index.html', context)


def join_group(request):
    """
    Agrega a un usuario a un grupo, ya sea una lista o una despensa

    Los codigos tendran vigencia definida en constants

    Propuesta:
    los codigos iniciados en 10 pertenecen a los inventarios
    los codigos iniciados en 01 pertenecen a las listas
    el resto del codigo esta por definir
    hacer una jsonresponse y mostrar codigo con ajax

    :param request:
    :return:
    """
    context = {}
    if request.method == 'POST':
        code = request.POST.get('code')
        if code[0] == '1' and code[1] == '0':
            code = codes.CodeInventory.objects.get(code=code)
            shared_object = code.inventory
        elif code[1] == '0' and code[0] == '0':
            code = codes.CodeShoppingCart.objects.get(code=code)
            shared_object = code.shopping_cart
        else:
            # FIXME: Hacer alguna cosa quizas ?? codigo no valido
            return
        if utils.time_delta(code.initial_date, constants.LIVE_CODE_DEFAULT) \
                >= constants.LIVE_CODE:
            # FIXME: do something, codigo expirado o algo por el estilo
            return
        shared_object.users.add(request.user)
        shared_object.save()
    #     TODO: redirigir a ubicacion del objeto agregado
    pass
