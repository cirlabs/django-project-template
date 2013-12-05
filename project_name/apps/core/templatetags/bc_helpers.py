from lxml import etree

from django.contrib.sites.models import Site
from django.template import Library
from django.template.defaultfilters import stringfilter

from cir.base.utils import get_current_protocol

register = Library()


@register.filter
def round_up_divide_by(value, amount):
    """Divide Value by Amount and round up. Return as int"""
    return int(round(float(value) / float(amount)))


@register.filter
@stringfilter
def remove_embeds(value):
    """Removes dropped_media <div> tags"""
    if not value:
        return ''

    doc = etree.HTML(value)
    embedded_divs = doc.xpath("//div[starts-with(@class,'dropped_media_')]")
    for div in embedded_divs:
        doc.remove(div)

    """The etree automagcially adds <HTML> and <BODY>
    tags to text it tries to parse. Removing them with a slice"""

    return etree.tostring(doc)[12:-14]


@register.filter
def subtract(value, arg):
    try:
        return int(value) - int(arg)
    except (TypeError, ValueError):
        return value

@register.simple_tag(takes_context=True)
def full_url(context, url):
    if url.startswith('http:') or url.startswith('https:'):
        return url

    request = context['request']
    protocol = get_current_protocol(request)
    protocol = 'https:'  #Remove once we get request.is_secure() working

    if not url.startswith('//'):
        url = '//%s%s' % (Site.objects.get_current().domain, url)

    return '%s%s' % (protocol, url)
