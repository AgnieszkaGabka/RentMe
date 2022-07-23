from django.shortcuts import render
from datetime import datetime, date

from django.contrib.auth import authenticate, login, logout
from django.core.checks import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

from .forms import ToRentForm, WantRentForm, LoginForm
from .models import ToRent


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


class RegisterView(View): #rejestracja nowego użytkownika

    def get(self, request):
        form = CreateUserForm()
        return render(request, 'register.html', {'form': form}) #formularz dodawania użytkownika

    def post(self, request):
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save() #jeśli dane się zgadzają, utwórz konto

            messages.Info(request, 'Twoje konto zostało utworzone poprawnie')
            return redirect('login')
        context = {'form': form}
        return render(request, 'register.html', context)


class BaseView(View):
    template_name = 'main.html'


class ToRentView(View):
    pass


class WantRentView(View):
    pass


class SearchResultView(View):
    model = ToRent
    template_name = 'main.html'