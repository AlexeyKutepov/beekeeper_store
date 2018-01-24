from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^contacts/$', views.contacts, name='contacts'),
    url(r'^add-to-cart/(?P<id>\d+)/$', views.add_to_cart, name='add_to_cart'),
    url(r'^delete-from-cart/(?P<id>\d+)/$', views.delete_from_cart, name='delete_from_cart'),
    url(r'^product/(?P<id>\d+)/$', views.product, name='product'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^create/order/$', views.create_order, name='create_order'),
    url(r'^order/(?P<id>\d+)/$', views.show_order, name='show_order'),
    url(r'^about/$', views.about, name='about'),
    url(r'^$', views.index, name='index'),
]