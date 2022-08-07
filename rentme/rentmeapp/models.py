from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models

from django.contrib.auth.models import User
from django.db.models import CASCADE

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


class Area(models.Model):
    pincode = models.CharField(validators=[MinLengthValidator(6), MaxLengthValidator(6)], max_length =6, unique=True)
    city = models.CharField(max_length=20)


class Seller(models.Model):
    seller = models.OneToOneField(User, on_delete=models.CASCADE)
    item = models.CharField(validators = [MinLengthValidator(10), MaxLengthValidator(13)], max_length = 13)
    area = models.OneToOneField(Area, on_delete=models.PROTECT)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.PROTECT)


class ToRent(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    category = models.IntegerField(choices=CATEGORY)
    name = models.CharField(max_length=256)
    date_from = models.DateField(blank=True)
    date_to = models.DateField(blank=True)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)
    price_day = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_available = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'things to rent to others'

    def __str__(self):
        return self.name


class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    rent = models.CharField(max_length=8)
    item = models.ForeignKey(ToRent, on_delete=models.PROTECT)
    days = models.CharField(max_length=3)

