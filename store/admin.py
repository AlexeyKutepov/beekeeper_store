# coding=utf-8
from django.contrib import admin

from store.models import Product, Cart


@admin.register(Product)
class Company(admin.ModelAdmin):
    """
    Товары
    """
    list_display = ('name', 'price', 'measure', 'in_stock')
    list_filter = ('name',)


@admin.register(Cart)
class Company(admin.ModelAdmin):
    """
    Корзина
    """
    list_display = ('session_key',)
    list_filter = ('session_key',)