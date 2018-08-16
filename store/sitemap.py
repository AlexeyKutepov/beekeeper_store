from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from store.models import Post, Product


class PostSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.update_date


class ProductSitemap(Sitemap):
    changefreq = "never"
    priority = 1

    def items(self):
        return Product.objects.filter(is_show=True)

    def lastmod(self, obj):
        return obj.update_date


class StaticSitemap(Sitemap):
    priority = 0.6
    changefreq = 'never'

    def items(self):
        return ['blog', 'contacts', 'about', 'photo', 'documents', 'delivery', 'index', ]

    def location(self, item):
        return reverse(item)