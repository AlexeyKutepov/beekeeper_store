# -*- coding: utf-8 -*-
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render


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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "sign_in.html", {"login_error": "has-error"})
    else:
        return render(request, "sign_in.html")


def control(request):
    return HttpResponseRedirect(reverse("index"))