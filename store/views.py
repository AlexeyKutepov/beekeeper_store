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
    cart_item_list = get_cart_item_list(request)
    return render(
        request,
        "index.html",
        {
            "product_list": product_list,
            "cart_size": len(cart_item_list)
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
    cart_item_list = get_cart_item_list(request)
    return render(
        request,
        "product.html",
        {
            "product": product,
            "cart_size": len(cart_item_list)
        }
    )


def cart(request):
    """
    Корзина
    :param request:
    :return:
    """
    cart_item_list = get_cart_item_list(request)
    return render(
        request,
        "cart.html",
        {
            "cart_item_list": cart_item_list,
            "cart_size": len(cart_item_list)
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


def delete_from_cart(request, id):
    """
    Удалить товар из корзины
    :param id: идентификатор товара
    :param request:
    :return:
    """
    CartItem.objects.get(id=id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def get_cart_item_list(request):
    """
    Возвращает список продуктов в корзине
    :param request:
    :return:
    """
    cart = Cart.objects.get_or_create(session_key=request.session.session_key)[0]
    return CartItem.objects.filter(cart=cart)


