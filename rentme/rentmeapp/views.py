from django.shortcuts import render
from datetime import datetime, date

from django.contrib.auth import authenticate, login, logout
from django.core.checks import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

from forms import ToRentForm, WantRentForm, LoginForm

class LoginView(View):

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        context = {
            'form': form
        }
        return render(request, 'login.html', context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_authenticated:
                login(request, user)
                messages.Info(request, "Jesteś zalogowany jako",  {user.username})
                return HttpResponseRedirect('/main/')
        messages.Error(request, "Błędny login lub hasło")
        return HttpResponseRedirect('/login/')


class BaseView(View):
    pass


class ToRentView(View):
    pass


class WantRentView(View):
    pass


class SearchView(View):
    pass