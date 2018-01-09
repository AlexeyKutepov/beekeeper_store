# coding=utf-8
from __future__ import unicode_literals

from django.db import models


class Product(models.Model):
    """
    Товар
    """
    kg = 'кг'
    pcs = 'шт'
    measure_classifier = (
        (kg, 'кг'),
        (pcs, 'шт'),
    )
    # Фото товара
    photo = models.ImageField(upload_to="images")
    # Название товара
    name = models.CharField(max_length=500)
    # Краткое описание
    short_description = models.TextField()
    # Полное описание
    description = models.TextField()
    # Цена
    price = models.FloatField()
    # Единица измерения
    measure = models.CharField(max_length=10, choices=measure_classifier, default=kg)
    # Флаг указывающий наличие товара на складе
    in_stock = models.BooleanField(default=True)


class Cart(models.Model):
    """
    Корзина с привязкой к сессии
    """
    session_key = models.CharField(max_length=500)


class CartItem(models.Model):
    """
    Элемент корзины
    """
    product = models.ForeignKey(Product)
    quantity = models.FloatField()
    cart = models.ForeignKey(Cart)


class Order(models.Model):
    """
    Заказ
    """
    accepted = 'Принят'
    execution = 'Исполнение'
    executed = 'Исполнен'
    canceled = 'Отменён'
    status_classifier = (
        (accepted, 'Принят'),
        (execution, 'Исполнение'),
        (executed, 'Исполнен'),
        (canceled, 'Отменён'),
    )
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=status_classifier, default=accepted)


class OrderItem(models.Model):
    """
    Элемент заказа
    """
    product = models.ForeignKey(Product)
    quantity = models.FloatField()
    order = models.ForeignKey(Order)



