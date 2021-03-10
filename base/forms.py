from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class Profilemodelform(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name',
                  'mobile_number', 'dp', 'payment_password']


class Postcreationform(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text_area', 'cash_required']


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['cash']
