from django.utils.feedgenerator import Rss201rev2Feed
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import striptags

from armstrong.core.arm_layout.utils import render_model


class BaseFeed(Feed):
    title_field = 'title'
    limit_items = 20

    # You'll probably want to implement these
        # def get_object(self, request, *args, **kwargs):
        # def description(self, obj):
        # def items(self, obj):

    def title(self, obj):
        return "The Bay Citizen - %s Feed" % getattr(obj, self.title_field)

    def link(self, obj):
        return obj.get_absolute_url()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return render_model(item, 'rss')

    def item_pubdate(self, item):
        return item.pub_date

    def item_author_name(self, item):
        # the single-source for sorting all the author stuff
        return striptags(render_model(item, 'author'))

