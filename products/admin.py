from django.contrib import admin

from products.models import Products, Cart_Products

# Register your models here.
admin.site.register(Products)
admin.site.register(Cart_Products)