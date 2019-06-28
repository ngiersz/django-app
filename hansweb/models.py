from django.db import models
from django.utils import timezone


class Order(models.Model):
    STATUS_CHOICES = (
        (0, 'WAITING_FOR_DELIVERER'),
        (1, 'IN_TRANSIT'),
        (2, 'CLOSED')
    )

    DIMENSION_CHOICES = (
        (0, 'Fits in a shoebox'),
        (1, 'Fits in a front seat of a car'),
        (2, 'Fits in a back seat of a car'),
        (3, 'Fits in a hatchback or SUV'),
        (4, 'Fits in a pickup truck')
    )

    client = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='client')
    deliverer = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='deliverer', blank=True, null=True, default='')
    pickupAddress = models.ForeignKey('hansweb.Address', on_delete=models.CASCADE, related_name='pickupAddress', default='')
    deliveryAddress = models.ForeignKey('hansweb.Address', on_delete=models.CASCADE, related_name='deliveryAddress', default='')
    title = models.CharField(max_length=100)
    description = models.TextField(default='')
    created_date = models.DateTimeField(
        default=timezone.now)
    price = models.FloatField(default=0.0)
    weight = models.FloatField(default=0.0)
    status = models.IntegerField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='WAITING_FOR_DELIVERER'
    )
    dimensions = models.IntegerField(
        max_length=1,
        choices=DIMENSION_CHOICES,
        default='Fits in a pickup truck'
    )
    isPaid = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Address(models.Model):
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=10)
    zip_code = models.CharField(max_length=6)

    def __str__(self):
        return self.street + ' ' + self.number + ', ' + self.zip_code + ' ' + self.city + ', ' + self.country

