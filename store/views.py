# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render

from store.models import Product, CartItem, Cart


def index(request):
    """
    Главная страница
    :param request:
    :return:
    """
    product_list = Product.objects.all()
    return render(
        request,
        "index.html",
        {
            "product_list": product_list
        }
    )


def contacts(request):
    """
    Контакты
    :param request:
    :return:
    """
    return render(request, "contacts.html")


def product(request, id):
    """
    Страница товара
    :param request:
    :param id: идентификатор товара
    :return: product.html
    """
    product = Product.objects.get(id=id)
    return render(
        request,
        "product.html",
        {
            "product": product
        }
    )


def add_to_cart(request, id, quantity):
    """
    Добавить товар в корзину
    :param id: идентификатор товара
    :param quantity: количество
    :param request:
    :return:
    """
    product = Product.objects.get(id=id)
    cart = Cart.objects.get_or_create(session_key=request.session.session_key)[0]
    CartItem.objects.create(product=product, quantity=quantity, cart=cart)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

