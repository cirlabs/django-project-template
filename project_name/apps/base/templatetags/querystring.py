from urllib import urlencode
from urlparse import urlparse, parse_qsl, ParseResult

from django import template
from django.utils.safestring import mark_safe


register = template.Library()

#TODO Django 1.4
# the following can be refactored using simple_tag()
# in 1.4 simple_tag() can use *args and **kwargs which makes this work

#
# modified from http://djangosnippets.org/snippets/1627/
#


def easy_tag(func):
    """Decorator to facilitate template tag creation"""
    def inner(parser, token):
        try:
            return func(*token.split_contents())
        except TypeError:
            raise template.TemplateSyntaxError('Bad arguments for tag "%s"'
                    % token.split_contents()[0])
    inner.__name__ = func.__name__
    inner.__doc__ = inner.__doc__
    return inner


class BuildParamsStringNode(template.Node):
    """
    Build a combined dictionary of queryparams from two sources.
    `initial_params` comes from the current request or the passed url.
    `dict_pairs` is parsed out of the call to the templatetag
    Params in `dict_pairs` take precedence over `initial_params`.

    Mash all the params together with comma separation.
    The value can be a string or a template variable.

        {% url_with_params "url" rel=0,wmode="transparent" %}
        {% url_with_params url_var rel=0,wmode=value_var %}
    """
    def __init__(self, params=None):
        self.dict_pairs = {}
        if params:
            for pair in params.split(','):
                pair = pair.split('=')
                self.dict_pairs[pair[0]] = template.Variable(pair[1])

    def build_params(self, context, initial_params):
        for key, value in self.dict_pairs.items():
            value = value.resolve(context)
            if value is None or value == '':
                del self.dict_pairs[key]
                if key in initial_params:
                    del initial_params[key]  # remove from original query as well
            else:
                self.dict_pairs[key] = value

        initial_params.update(self.dict_pairs)
        return initial_params


class BuildSelfUrlStringNode(BuildParamsStringNode):
    """Add queryparams to the current page URL and coexist with any params already in the request"""

    def render(self, context):
        request = context['request']
        params = request.POST.copy() if request.method == "POST" else request.GET.copy()

        url = request.path_info
        final_params = self.build_params(context, params)

        if final_params:
            return mark_safe("%s?%s" % (url, urlencode(final_params)))
        return mark_safe(url)


class BuildUrlStringNode(BuildParamsStringNode):
    """Add queryparams to a URL that may also include params"""

    def __init__(self, url, params=None):
        self.url = template.Variable(url)
        super(BuildUrlStringNode, self).__init__(params)

    def render(self, context):
        url = self.url.resolve(context)
        parsed = urlparse(url)
        params = dict(parse_qsl(parsed.query))  # only allow one value per key (not the list that parse_qs() gives)

        final_params = self.build_params(context, params)
        new_url = ParseResult(
                    parsed.scheme,
                    parsed.netloc,
                    parsed.path,
                    parsed.params,
                    urlencode(final_params),
                    parsed.fragment)

        return mark_safe(new_url.geturl())


@register.tag()
@easy_tag
def self_with_params(_tag_name, params=None):
    return BuildSelfUrlStringNode(params)


@register.tag()
@easy_tag
def url_with_params(_tag_name, url, params=None):
    return BuildUrlStringNode(url, params)
