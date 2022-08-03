from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from rentmeapp import views

from rentmeapp.views import HomePageView, AddItemView

urlpatterns = [
    url('home/', HomePageView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('auth/', views.auth_view, name='auth_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('register/', views.register, name='register'),
    path('registration/', views.registration, name='registration'),
    path('add_item/', AddItemView.as_view(), name='add_item'),
    path('manage_orders/', views.manage_orders, name='manage_orders'),
    path('manage_items/', views.manage_items, name='manage_items'),
    path('order_list/', views.order_list, name='order_list'),
    path('search/', views.search, name='search'),
    path('search_results/', views.search_results, name='search_results'),
    path('rent/', views.rent_item, name='rent_item'),
    path('confirmed/', views.confirm, name='confirm'),
    path('update-order/', views.update_order, name='update_order'),
    path('delete-order/', views.delete_order, name='delete_order'),
    path('update-item/', views.update_item, name='update_item'),
    path('delete-item/', views.delete_item, name='delete_item'),
]
