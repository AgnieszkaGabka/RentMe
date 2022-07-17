from django.db import models


CATEGORY = (
    (1, "narzędzia do naprawy domu"),
    (2, "sprzęt samochodowy"),
    (3, "sprzęt AGD"),
    (4, "rzeczy kuchenne"),
    (5, "narzędzia ogrodowe"),
    (6, "meble"),
    (7, "samochody"),
    (8, "rzeczy dla dzieci")
)


class ToRent(models.Model):
    category = models.IntegerField(choices=CATEGORY)
    name = models.CharField(max_length=256)
    date_from = models.DateField(auto_now_add=True, blank=True)
    date_to = models.DateField(blank=True)
    price_day = models.DecimalField(max_digits=5, decimal_places=2, default=0)


class WantRent(models.Model):
    category = models.IntegerField(choices=CATEGORY)
    name = models.CharField(max_length=256)
    date_from = models.DateField(auto_now_add=True, blank=True)
    date_to = models.DateField(blank=True)
    price_day_from = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    price_day_to = models.DecimalField(max_digits=5, decimal_places=2, default=0)
