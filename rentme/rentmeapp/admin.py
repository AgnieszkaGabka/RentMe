from django.contrib import admin
from .models import Area, Seller, Customer, ToRent, WantRent, Orders

admin.site.register(Area)
admin.site.register(Seller)
admin.site.register(Customer)
admin.site.register(ToRent)
admin.site.register(WantRent)
admin.site.register(Orders)

