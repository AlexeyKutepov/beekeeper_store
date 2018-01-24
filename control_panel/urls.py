from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^signin/$', views.sign_in, name='sign_in'),
    url(r'^control/$', views.control, name='control'),
    url(r'^control/order/(?P<id>\d+)/$', views.control_order, name='control_order'),
    url(r'^change/order/status/(?P<id>\d+)/$', views.change_order_status, name='change_order_status'),
]