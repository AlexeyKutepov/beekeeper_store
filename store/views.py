# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from store.models import Product, CartItem, Cart, Order, OrderItem


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
        "store/index.html",
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
    return render(request, "store/contacts.html")


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
        "store/product.html",
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
        "store/cart.html",
        {
            "cart_item_list": cart_item_list,
            "cart_size": len(cart_item_list)
        }
    )


def add_to_cart(request, id):
    """
    Добавить товар в корзину
    :param id: идентификатор товара
    :param quantity: количество
    :param request:
    :return:
    """
    if not request.session.session_key:
        request.session.save()
    if "quantity" in request.POST:
        quantity = request.POST.get("quantity")
        product = Product.objects.get(id=id)
        cart = Cart.objects.get_or_create(session_key=request.session.session_key)[0]
        CartItem.objects.create(product=product, quantity=quantity, cart=cart)
    return HttpResponseRedirect(reverse("cart"))


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
    if not request.session.session_key:
        request.session.save()
    cart = Cart.objects.get_or_create(session_key=request.session.session_key)[0]
    return CartItem.objects.filter(cart=cart)


def create_order(request):
    """
    Оформить заказ
    :param request:
    :return:
    """
    if not request.session.session_key:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    cart = Cart.objects.get_or_create(session_key=request.session.session_key)[0]
    cart_item_list = CartItem.objects.filter(cart=cart)
    if cart_item_list and len(cart_item_list) > 0:
        email = None
        phone = None
        if "email" in request.POST:
            email = request.POST.get("email")
        if "phone" in request.POST:
            phone = request.POST.get("phone")
        order = Order.objects.create(email=email, phone=phone)
        for item in cart_item_list:
            OrderItem.objects.create(product=item.product, quantity=item.quantity, order=order)
            item.delete()
        cart.delete()
        return HttpResponseRedirect(reverse("show_order", args=[order.id,]))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def show_order(request, id):
    order = Order.objects.get(id=id)
    order_item_list = OrderItem.objects.filter(order=order)
    return render(
        request,
        "store/order.html",
        {
            "order": order,
            "order_item_list": order_item_list,
        }
    )


def about(request):
    return render(
        request,
        "store/about.html"
    )