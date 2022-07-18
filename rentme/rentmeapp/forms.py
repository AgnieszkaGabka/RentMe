from django import forms

from models import CATEGORY, ToRent, WantRent
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AddToRent(forms.ModelForm):

    class Meta:
        model = ToRent
        exclude = ("user",)

    category = forms.IntegerField(choices=CATEGORY, widget=forms.SelectMultiple())
    name = forms.CharField()
    date_from = forms.DateField(input_formats=["%Y-%m-%d"])
    date_to = forms.DateField(input_formats=["%Y-%m-%d"])
    price_day = forms.DecimalField()


class AddWantRent:

    class Meta:
        model = WantRent

    category = forms.IntegerField(choices=CATEGORY, widget=forms.SelectMultiple())
    name = forms.CharField()
    date_from = forms.DateField(input_formats=["%Y-%m-%d"])
    date_to = forms.DateField(input_formats=["%Y-%m-%d"])
    price_day_from = forms.DecimalField()
    price_day_to = forms.DecimalField()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)