from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^contacts/$', views.contacts, name='contacts'),
    url(r'^add-to-cart/(?P<id>\d+)/(?P<quantity>\d+)/$', views.add_to_cart, name='add_to_cart'),
    url(r'^$', views.index, name='index'),
]