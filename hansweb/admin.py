from django.contrib import admin
from .models import Order, Address


class OrderAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'client', 'deliverer', 'created_date', 'isPaid', 'pickupAddress', 'deliveryAddress')
    search_fields = ['title']
    readonly_fields = ()

    filter_horizontal = []
    list_filter = ['status']
    fieldsets = ()


admin.site.register(Order, OrderAdmin)
admin.site.register(Address)
