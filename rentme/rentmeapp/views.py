from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.defaulttags import csrf_token

from .models import ToRent, Customer, Area, Orders, WantRent


def home_page(request):
    return render(request, 'index.html')


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    else:
        return render(request, 'home_page.html')


def login(request):
    return render(request, 'login.html')


def auth_view(request):
    if request.user.is_authenticated:
        return render(request, 'home_page.html')
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
            return render(request, 'home_page.html')
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
    mobile = request.POST['mobile']
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    email = request.POST['email']
    city = request.POST['city']
    city = city.lower()
    pincode = request.POST['pincode']
    try:
        user = User.objects.create_user(username=username, password=password, email=email)
        user.first_name = firstname
        user.last_name = lastname
        user.save()
    except:
        return render(request, 'registration_error.html')
    try:
        area = Area.objects.get(city=city, pincode=pincode)

    except:
        area = None
    if area is not None:
        customer = Customer(user=user, mobile=mobile, area=area)
    else:
        area = Area(city=city, pincode=pincode)
        area.save()
        area = Area.objects.get(city=city, pincode=pincode)
        customer = Customer(user=user, mobile=mobile, area=area)

    customer.save()
    return render(request, 'registered.html')


@login_required
def search(request):
    return render(request, 'search.html')


@login_required
def search_results(request):
    city = request.POST['city']
    city = city.lower()
    items_list = []
    area = Area.objects.filter(city=city)
    for a in area:
        items = ToRent.objects.filter(area=a)
        for item in items:
            if item.is_available:
                item_dictionary = {'user': item.user, 'category': item.category, 'name': item.name,
                                   'date_from': item.date_from, 'date_to': item.date_to, 'price_day': item.price_day}
                items_list.append(item_dictionary)
    request.session['items_list'] = items_list
    return render(request, 'search_results.html')


@login_required
def rent_item(request):
    item_id = request.POST['id']
    item = ToRent.objects.get(id=item_id)
    price_day = int(item.price_day)
    return render(request, 'confirmation.html', {'item': item, 'price_day': price_day})


@login_required
def confirm(request):
    item_id = request.POST['id']
    username = request.user
    user = User.objects.get(username=username)
    days = request.POST['days']
    item = ToRent.objects.get(id=item_id)
    if item.is_available:
        rent = int(days)
        try:
            order = Orders(item=item, user=user, rent=rent, days=days)
            order.save()
        except:
            order = Orders.objects.get(item=item, user=user, rent=rent, days=days)
        item.is_available = False
        item.save()
        return render(request, 'confirmed.html', {'order':order})
    else:
        return render(request, 'order_failed.html')


@login_required
def manage(request):
    order_list = []
    user = User.objects.get(username=request.user)
    try:
        orders = Orders.objects.filter(user=user)
    except:
        orders = None
    if orders is not None:
        for o in orders:
            if not o.is_complete:
                order_dictionary = {'id':o.id,'rent':o.rent, 'item':o.item, 'days':o.days}
                order_list.append(order_dictionary)
    return render(request, 'manage.html', {'od':order_list})


@login_required
def update_order(request):
    order_id = request.POST['id']
    order = Orders.objects.get(id=order_id)
    item = order.item
    item.is_available = True
    item.save()
    order.delete()
    cost_day = item.price_day
    return render(request, 'confirmation.html', {'item': item}, {'cost_day': cost_day})


@login_required
def delete_order(request):
    order_id = request.POST['id']
    order = Orders.objects.get(id=order_id)
    item = order.item
    item.is_available = True
    item.save()
    order.delete()
    return HttpResponseRedirect('/manage/')


@login_required
def add_item(request):
    category = request.post['category']
    name = request.POST['name']
    date_from = request.POST['date_from']
    date_to = request.POST['date_to']
    city = request.POST['city']
    city = city.lower()
    pincode = request.POST['pincode']
    price_day = request.POST['price_day']
    try:
        area = Area.objects.get(city = city, pincode = pincode)
    except:
        area = None
    if area is not None:
        item = WantRent(category=category, name=name, date_from=date_from, date_to=date_to, area = area,
                        price_day = price_day)
    else:
        area = Area(city = city, pincode = pincode)
        area.save()
        area = Area.objects.get(city = city, pincode = pincode)
        item = WantRent(category=category, name=name, date_from=date_from, date_to=date_to, area = area,
                        price_day = price_day)
    item.save()
    return render(request, 'item_added.html')

@login_required
def manage_vehicles(request):
    username = request.user
    user = User.objects.get(username = username)
    items_list = []
    my_items = WantRent.objects.filter(user = user)
    for i in my_items:
        items_list.append(i)
    return render(request, 'manage.html', {'items_list':items_list})

@login_required
def order_list(request):
    username = request.user
    user = User.objects.get(username = username)
    orders = Orders.objects.filter(user = user)
    order_list = []
    for o in orders:
        if o.is_complete == False:
            order_list.append(o)
    return render(request, 'order_list.html', {'order_list': order_list})


@login_required
def delete(request):
    item_id = request.POST['id']
    item = WantRent.objects.get(id=item_id)
    item.delete()
    return HttpResponseRedirect('/manage_items/')