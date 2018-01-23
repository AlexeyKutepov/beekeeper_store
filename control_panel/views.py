# -*- coding: utf-8 -*-
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from store.models import Order, OrderItem


def sign_in(request):
    """
    Авторизация
    :param request:
    :return:
    """
    if "login" in request.POST and "password" in request.POST:
        username = str(request.POST.get("login")).strip()
        password = str(request.POST.get("password")).strip()
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse("control"))
        else:
            return render(request, "control_panel/sign_in.html", {"login_error": "has-error"})
    else:
        return render(request, "control_panel/sign_in.html")


def control(request):
    order_list = Order.objects.all().order_by('-date')
    return render(
        request,
        "control_panel/control_panel.html",
        {
            "order_list": order_list
        }
    )


def control_order(request, id):
    order = Order.objects.get(id=id)
    order_item_list = OrderItem.objects.filter(order=order)
    return render(
        request,
        "control_panel/order.html",
        {
            "order": order,
            "order_item_list": order_item_list,
        }
    )