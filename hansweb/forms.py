from django import forms
from .models import Order


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
