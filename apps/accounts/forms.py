from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'Correo electronico', 'class': 'form-control', 'icon':
            'fas fa-at'}), )

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
