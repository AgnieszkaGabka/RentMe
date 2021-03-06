from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from rentmeapp import views

from rentmeapp.views import HomePageView

urlpatterns = [
    url('home/', HomePageView.as_view(), name='home_page'),
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('auth/', views.auth_view, name='auth_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('register/', views.register, name='register'),
    path('registration/', views.registration, name='registration'),
    path('add_item/', views.add_item, name='add_item'),
    path('manage/', views.manage, name='manage'),
    path('manage_items/', views.manage_items, name='manage_items'),
    path('order_list/', views.order_list, name='order_list'),
    #path('complete/', views.complete, name='complete'),
    path('search/', views.search, name='search'),
    path('search_results/', views.search_results, name='search_results'),
    path('rent/', views.rent_item, name='rent_item'),
    path('confirmed', views.confirm, name='confirm'),
    path('update', views.update_order, name='update_order'),
    path('delete/', views.delete_order, name='delete_order'),
]
