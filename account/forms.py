from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import ModelForm

from account.models import User, Profile, BecomeSeller


class CreateAnAccountForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'span12', 'placeholder': 'Enter Your Email'}),
            'password1': forms.PasswordInput(attrs={'class': 'span12', 'placeholder': '********'}),
            'password2': forms.PasswordInput(attrs={'class': 'span12', 'placeholder': '********'}),
            
        }


class ProfileInfoForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('__all__')
        exclude = ('user',)


class BecomeSellerForm(ModelForm):
    class Meta:
        model = BecomeSeller
        fields = ('__all__')

