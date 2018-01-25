# coding=utf-8
from django.contrib import admin

from store.models import Product, Cart, Order, OrderItem, CartItem, Feedback, Photo


@admin.register(Product)
class Product(admin.ModelAdmin):
    """
    Товары
    """
    list_display = ('name', 'price', 'measure', 'in_stock')
    list_filter = ('name',)


@admin.register(Cart)
class Cart(admin.ModelAdmin):
    """
    Корзина
    """
    list_display = ('session_key',)
    list_filter = ('session_key',)

@admin.register(CartItem)
class CartItem(admin.ModelAdmin):
    """
    Элемент заказа
    """
    list_display = ('cart', 'product', 'quantity',)
    list_filter = ('cart',)


@admin.register(Order)
class Order(admin.ModelAdmin):
    """
    Заказ
    """
    list_display = ('phone', 'email', 'date', 'status',)
    list_filter = ('date',)


@admin.register(OrderItem)
class OrderItem(admin.ModelAdmin):
    """
    Элемент заказа
    """
    list_display = ('order', 'product', 'quantity',)
    list_filter = ('order',)


@admin.register(Feedback)
class Feedback(admin.ModelAdmin):
    """
    Обратная связь
    """
    list_display = ('name', 'phone', 'email', 'message', 'date',)
    list_filter = ('date',)


@admin.register(Photo)
class Photo(admin.ModelAdmin):
    """
    Фотографии
    """
    list_display = ('name', 'date',)
    list_filter = ('date',)