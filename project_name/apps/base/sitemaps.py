# using this to get `item` attribute in the template
# so we can use it for the Google News template
from django.contrib.sitemaps import Sitemap

from cir.bc_content.models import BCContent


class BaseSitemap(Sitemap):
    def __init__(self, **kwargs):
        # allow these standard attributes to be passed on instantiation
        self.changefreq = kwargs.get('changefreq')
        self.priority = kwargs.get('priority')

    def lastmod(self, obj):
        # 1. obj has a publish date
        if hasattr(obj, 'pub_date'):
            return obj.pub_date

        """
        Use the latest content item to determine the update time

        NOTE: This is slow. It performs a query for every single `obj` so
        a) either comment this method out and don't use it or
        b) cache heavily (daily or longer; anything more precise is useless)

        """
        # 2. filter BCContent based on this obj
        # class must define the name of the filter field
        if hasattr(self, 'filter_field'):
            filters = {self.filter_field: obj}
            try:
                return BCContent.published.filter(**filters).only('pub_date')[0].pub_date
            except IndexError:
                pass

        # 3. default to not using `lastmod`
        return None
