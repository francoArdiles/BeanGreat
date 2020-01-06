from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )
        widgets = {
            'username': forms.TextInput(attrs={'id': 'reg_username'}),
        }

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        if self.is_valid():
            user.email = self.cleaned_data['email']
        if commit:
            user.save()

        return user
