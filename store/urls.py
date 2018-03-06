from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^contacts/$', views.contacts, name='contacts'),
    url(r'^add-to-cart/(?P<id>\d+)/$', views.add_to_cart, name='add_to_cart'),
    url(r'^delete-from-cart/(?P<id>\d+)/$', views.delete_from_cart, name='delete_from_cart'),
    url(r'^product/(?P<id>\d+)/$', views.product, name='product'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^create/order/$', views.create_order, name='create_order'),
    url(r'^order/(?P<id>\d+)/(?P<uuid>[0-9a-f-]+)/$', views.show_order, name='show_order'),
    url(r'^about/$', views.about, name='about'),
    url(r'^photo/$', views.photo, name='photo'),
    url(r'^documents/$', views.documents, name='documents'),
    url(r'^delivery/$', views.delivery, name='delivery'),
    url(r'^feedback/$', views.feedback, name='feedback'),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    url(r'^$', views.index, name='index'),
]