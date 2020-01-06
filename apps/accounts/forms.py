from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'Correo electronico', 'class': 'form-control', 'icon':
            'fas fa-at'}), help_text='Obligatorio. Introduzca su correo '
                                     'electrónico. Debe ser una dirección '
                                     'válida')

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )

        widgets = {
            'username': forms.TextInput(attrs={'id': 'reg_username',
                                               'placeholder': 'Nombre de '
                                                              'usuario',
                                               'class': 'form-control',
                                               'icon': 'fas fa-user'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'icon': 'fas fa-lock',
                   'placeholder': 'contraseña'})
        self.fields['password1'].help_text = 'Introduzca su contraseña. Debe ' \
                                             'contener al menos 8 caracteres.' \
                                             ' No pueden ser sólo números. No' \
                                             ' debe ser una contraseña usada ' \
                                             'comunmente. No puede ser muy ' \
                                             'similar a su otra informacón' \
                                             ' personal'
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'icon': 'fas fa-lock',
                   'placeholder': 'Repita contraseña'})

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        if self.is_valid():
            user.email = self.cleaned_data['email']
        if commit:
            user.save()

        return user
