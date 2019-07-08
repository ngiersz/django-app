from django import forms
from .models import Order, Address


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('title',
                  'pickupAddress',
                  'deliveryAddress',
                  'description',
                  'weight',
                  'dimensions',
                  'price',
                  'isPaid')


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('country',
                  'city',
                  'street',
                  'number',
                  'zip_code')
