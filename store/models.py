# coding=utf-8
import uuid

from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone

from django.db import models


class Product(models.Model):
    """
    Товар
    """
    kg = u'кг'
    pcs = u'шт'
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
    # Отображать товар
    is_show = models.BooleanField(default=True)
    # Порядковый номер товара
    order_number = models.IntegerField(default=0)
    # Дата обновления
    update_date = models.DateTimeField(default=timezone.now)


    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/product/%i/" % self.id


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
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20)
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=status_classifier, default=accepted)

    def __unicode__(self):
        return self.phone

    def __str__(self):
        return self.phone


class OrderItem(models.Model):
    """
    Элемент заказа
    """
    product = models.ForeignKey(Product)
    quantity = models.FloatField()
    order = models.ForeignKey(Order)


class Feedback(models.Model):
    """
    Обратная связь
    """
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Photo(models.Model):
    """
    Фотографии
    """
    name = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now)
    photo = models.ImageField(upload_to="photos")

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class NotificationEmail(models.Model):
    """
    Адреса для уведомлений
    """
    email = models.EmailField()

    def __unicode__(self):
        return self.email

    def __str__(self):
        return self.email


class Post(models.Model):
    """
    Пост
    """
    title = models.CharField(max_length=500, default="Title")
    title_image = models.ImageField(upload_to="title_images")
    date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(default=timezone.now)
    short_text = models.TextField()
    content = RichTextUploadingField('contents')

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/post/%i/" % self.id