# coding=utf-8
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from store.models import Product, Cart, Order, OrderItem, CartItem, Feedback, Photo, NotificationEmail, Post


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


@admin.register(NotificationEmail)
class NotificationEmail(admin.ModelAdmin):
    """
    Адреса для уведомлений
    """
    list_display = ('email',)
    list_filter = ('email',)


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm


admin.site.register(Post, PostAdmin)
