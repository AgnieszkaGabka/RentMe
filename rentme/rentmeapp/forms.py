from django import forms

from .models import CATEGORY, ToRent, WantRent
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ToRentForm(forms.ModelForm):

    class Meta:
        model = ToRent
        exclude = ("user",)

    category = forms.IntegerField(widget=forms.SelectMultiple())
    name = forms.CharField()
    date_from = forms.DateField(input_formats=["%Y-%m-%d"])
    date_to = forms.DateField(input_formats=["%Y-%m-%d"])
    price_day = forms.DecimalField()


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class WantRentForm:

    class Meta:
        model = WantRent

    category = forms.IntegerField(widget=forms.SelectMultiple())
    name = forms.CharField()
    date_from = forms.DateField(input_formats=["%Y-%m-%d"])
    date_to = forms.DateField(input_formats=["%Y-%m-%d"])
    price_day_from = forms.DecimalField()
    price_day_to = forms.DecimalField()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)