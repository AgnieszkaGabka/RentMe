from django.contrib import admin

from .models import ToRent

class ToRentAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_from', 'date_to', 'price_day')


admin.site.register(ToRent, ToRentAdmin)
