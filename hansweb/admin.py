from django.contrib import admin
from .models import Order, Address
from users.models import User

admin.site.register(Order)
admin.site.register(Address)
admin.site.register(User)
