from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.defaulttags import csrf_token
from django.utils.datastructures import MultiValueDictKeyError
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .forms import ToRentForm, UpdateOrderForm
from .models import ToRent, Customer, Area, Orders


class HomePageView(View):
    def get(self, request):
        form = ToRentForm()
        return render(request, 'home_page.html', {'form': form})

    def post(self, request):
        form = ToRentForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            category = form.cleaned_data['category']
            name = form.cleaned_data['name']
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            area = form.cleaned_data['area']
            price_day = form.cleaned_data['price_day']
            item = ToRent.objects.create(user=user, category=category, name=name, date_from=date_from, date_to=date_to,
                                         area=area, price_day=price_day)
            item.save()
            return render(request, 'manage_items.html')
        else:
            return redirect(f'/home/')


def login(request):
    return render(request, 'login.html')


def auth_view(request):
    if request.user.is_authenticated:
        form = ToRentForm()
        return render(request, 'home_page.html', {'form': form})
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        try:
            customer = Customer.objects.get(user=user)
        except:
            customer = None
        if customer is not None:
            auth.login(request, user)
            form = ToRentForm()
            return render(request, 'home_page.html', {'form': form})
        else:
            return render(request, 'login_failed.html')


def logout_view(request):
    auth.logout(request)
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def registration(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    city = request.POST['city']
    city = city.lower()
    pincode = request.POST['pincode']
    try:
        user = User.objects.get(username=username, password=password, email=email)
        return render(request, 'registration_error.html')
    except User.DoesNotExist:
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
    try:
        area = Area.objects.get(city=city, pincode=pincode)
        customer = Customer(user=user, area=area)
    except Area.DoesNotExist:
        area = Area(city=city, pincode=pincode)
        area.save()
        area = Area.objects.get(city=city, pincode=pincode)
        customer = Customer(user=user, area=area)

    customer.save()
    return render(request, 'registered.html')


def search(request):
    return render(request, 'search.html')


def search_results(request):
    city = request.POST['city']
    items_list = []
    try:
        area = Area.objects.get(city=city)
    except Area.DoesNotExist:
        return render(request, 'search.html')
    items = ToRent.objects.filter(area=area)
    for item in items:
        if item.is_available:
            items_list.append(item)
    return render(request, 'search_results.html', {'items_list': items_list})


@login_required
def rent_item(request):
    item_id = request.POST['id']
    item = ToRent.objects.get(id=item_id)
    price_day = int(item.price_day)
    return render(request, 'confirmation_order.html', {'item': item, 'price_day': price_day})


@login_required
@csrf_exempt
def confirm(request):
    item_id = request.POST['id']
    user = request.user
    days = request.POST['days']
    item = ToRent.objects.get(id=item_id)
    if item.is_available:
        rent = int(days) * int(item.price_day)
        try:
            order = Orders(item=item, user=user, rent=rent, days=days)
            order.save()
        except:
            order = Orders.objects.get(item=item, user=user, rent=rent, days=days)
        item.is_available = False
        item.save()
        return render(request, 'confirmed.html', {'order': order})
    else:
        return render(request, 'order_failed.html')


@login_required
@csrf_exempt
def manage_orders(request):
    order_list = []
    user = request.user
    orders = Orders.objects.filter(user=user)
    if orders is not None:
        for o in orders:
            order_dictionary = {'id': o.id, 'rent': o.rent, 'item': o.item, 'days': o.days}
            order_list.append(order_dictionary)
    return render(request, 'manage_orders.html', {'od': order_list})

@login_required
@csrf_exempt
def update_order(request):
    id = request.POST['id']
    order = Orders.objects.get(id=id)
    cost = int(order.days) * int(order.item.price_day)
    order.save()
    return render(request, 'manage_orders.html', {'order': order, 'cost': cost})


@login_required
@csrf_exempt
def update_item(request):
    item_id = request.POST['id']
    item = ToRent.objects.get(id=item_id)
    item.is_available = True
    item.save()
    cost_day = item.price_day
    return render(request, 'confirmation_item.html', {'item': item}, {'cost_day': cost_day})


@login_required
@csrf_exempt
def delete_order(request):
    order_id = request.POST['id']
    order = Orders.objects.get(id=order_id)
    item = order.item
    item.is_available = True
    item.save()
    order.delete()
    return HttpResponseRedirect('/manage-orders/')


@login_required
@csrf_exempt
def delete_item(request):
    item_id = request.POST['id']
    item = ToRent.objects.get(id=item_id)
    item.is_available = True
    item.save()
    item.delete()
    return HttpResponseRedirect('/manage-items/')


class AddItemView(View):

    def get(self, request):
        user = request.user
        form = ToRentForm()
        return render(request, 'add_item.html', {'form': form})

    def post(self, request):
        user = request.user
        form = ToRentForm(request.POST)
        if form.is_valid():
            category = request.POST['category']
            name = form.cleaned_data['name']
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            area = form.cleaned_data['area']
            price_day = form.cleaned_data['price_day']
            item = ToRent(user=user, category=category, name=name, date_from=date_from, date_to=date_to, area=area,
                              price_day=price_day)
            item.save()
            return render(request, 'manage_items.html')
        return redirect(f'/home/')


@login_required
@csrf_exempt
def manage_items(request):
    username = request.user
    user = User.objects.get(username=username)
    items_list = []
    my_items = ToRent.objects.filter(user=user)
    for i in my_items:
        items_list.append(i)
    return render(request, 'manage_items.html', {'items_list': items_list})


@login_required
@csrf_exempt
def delete(request):
    item_id = request.POST['id']
    item = ToRent.objects.get(id=item_id)
    item.delete()
    return HttpResponseRedirect('/manage_items/')
