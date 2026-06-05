from django.contrib import admin
from .models import Product, Order
from django.contrib.auth.models import Group

admin.site.site_header = 'Inventory Dashboard'


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity')
    search_fields = ('name', 'category')
    list_filter = ('category',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'order_quantity', 'staff', 'order_date', 'status')
    search_fields = ('product__name', 'staff__username', 'status')
    list_filter = ('status', 'order_date')


# Register models
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)

# admin.site.unregister(Group)