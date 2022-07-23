from django.contrib import admin
from django.urls import path


from rentmeapp.views import BaseView, ToRentView, WantRentView, LoginView, RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', BaseView.as_view(), name='main'),
    path('login/', LoginView.as_view(), name='login'),
    path('add-item', ToRentView.as_view, name='add_item'),
    path('add-rent', WantRentView.as_view, name='add_rent'),
    path('register/', RegisterView.as_view(), name='register'),
]
