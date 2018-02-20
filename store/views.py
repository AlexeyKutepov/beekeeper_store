# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from beekeeper_store import settings
from store.models import Product, CartItem, Cart, Order, OrderItem, Feedback, Photo, NotificationEmail


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
    cart_item_list = get_cart_item_list(request)
    return render(request, "store/contacts.html", {"cart_size": len(cart_item_list),})


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
    sum_cart = 0
    for item in cart_item_list:
        sum_cart += item.quantity * item.product.price
    return render(
        request,
        "store/cart.html",
        {
            "cart_item_list": cart_item_list,
            "cart_size": len(cart_item_list),
            "sum_cart": sum_cart
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
        send_billing_email(request, order)
        return HttpResponseRedirect(reverse("show_order", args=[order.id, order.uuid]))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def show_order(request, id, uuid):
    """
    Показать заказ
    :param request:
    :param id: идентификатор заказа
    :return:
    """
    order = Order.objects.get(id=id, uuid=uuid)
    order_item_list = OrderItem.objects.filter(order=order)
    cart_item_list = get_cart_item_list(request)
    sum_order = 0
    for item in order_item_list:
        sum_order += item.quantity * item.product.price
    return render(
        request,
        "store/order.html",
        {
            "order": order,
            "order_item_list": order_item_list,
            "cart_size": len(cart_item_list),
            "sum_order": sum_order
        }
    )


def about(request):
    """
    Обо мне
    :param request:
    :return:
    """
    cart_item_list = get_cart_item_list(request)
    return render(
        request,
        "store/about.html",
        {
            "cart_size": len(cart_item_list)
        }
    )


def photo(request):
    """
    Фото
    :param request:
    :return:
    """
    cart_item_list = get_cart_item_list(request)
    photo_list = Photo.objects.all()
    return render(
        request,
        "store/photo.html",
        {
            "cart_size": len(cart_item_list),
            "photo_list": photo_list
        }
    )


def documents(request):
    """
    Документы
    :param request:
    :return:
    """
    cart_item_list = get_cart_item_list(request)
    return render(
        request,
        "store/documents.html",
        {
            "cart_size": len(cart_item_list)
        }
    )


def feedback(request):
    """
    Фидбэк
    :param request:
    :return:
    """
    if "name" in request.POST and "email" in request.POST and "phone" in request.POST and "message" in request.POST:
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        Feedback.objects.create(name=name, email=email, phone=phone, message=message)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def send_billing_email(request, order):
    order_item_list = OrderItem.objects.filter(order=order)
    sum_order = 0
    order_url = request.build_absolute_uri(reverse("show_order", args=[order.id, order.uuid]))
    for item in order_item_list:
        sum_order += item.quantity * item.product.price
    msg_plain = "Благодарим Вас за покупку в интернет-магазине пчеловода Рязанцева! Статус заказа Вы можете отслеживать по ссылке: " + order_url
    msg_html = render_to_string('email/billing.html', {'order': order, "order_item_list": order_item_list, "sum_order": sum_order, "order_url": order_url})

    notification_email = NotificationEmail.objects.all()
    notification_list = [order.email]
    for item in notification_email:
        notification_list.append(item.email)

    send_mail(
        'Заказ №' + str(order.id),
        msg_plain,
        getattr(settings, "EMAIL_HOST_USER", None),
        notification_list,
        html_message=msg_html,
    )


def delivery(request):
    """
    Доставка
    :param request:
    :return:
    """
    cart_item_list = get_cart_item_list(request)
    return render(
        request,
        "store/delivery.html",
        {
            "cart_size": len(cart_item_list)
        }
    )