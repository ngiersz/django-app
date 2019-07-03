from django.db import models
from django.utils import timezone
from djchoices import DjangoChoices, ChoiceItem


class Order(models.Model):

    class StatusType(DjangoChoices):
        waiting = ChoiceItem(label="Waiting for deliverer")
        transit = ChoiceItem(label="In transit")
        closed = ChoiceItem(label="Closed")

    class DimensionType(DjangoChoices):
        shoebox = ChoiceItem(label="Fits in a shoebox")
        front_seat = ChoiceItem(label="Fits in a front seat of a car")
        back_seat = ChoiceItem(label="Fits in a back seat of a car")
        hatchback = ChoiceItem(label="Fits in a hatchback or SUV")
        pickup = ChoiceItem(label="Fits in a pickup truck")

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
    status = models.CharField(
        max_length=15,
        choices=StatusType.choices,
        default=StatusType.waiting
    )
    dimensions = models.CharField(
        max_length=30,
        choices=DimensionType.choices,
        default=DimensionType.pickup
    )
    isPaid = models.BooleanField()

    def __str__(self):
        return self.title

    def accept(self, user_deliverer):
        self.status = self.StatusType.transit
        self.deliverer = user_deliverer

    def close(self):
        self.status = self.StatusType.closed
        self.isPaid = True

    def can_delete(self):
        return self.status == self.StatusType.waiting


class Address(models.Model):
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=10)
    zip_code = models.CharField(max_length=6)

    def __str__(self):
        return self.street + ' ' + self.number + ', ' + self.zip_code + ' ' + self.city + ', ' + self.country

    # formatted = without zip_code and flat number
    def get_formatted(self):
        if '/' in self.number:
            return '{} {}, {}, {}'.format(self.street, self.number.split('/')[0], self.city, self.country)
        return '{} {}, {}, {}'.format(self.street, self.number, self.city, self.country)



