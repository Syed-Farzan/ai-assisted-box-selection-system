from django.contrib import admin

from .models import Box, Order, OrderItem, Product

admin.site.register(Box)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
