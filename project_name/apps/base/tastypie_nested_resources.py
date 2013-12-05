"""
From: https://gist.github.com/dhui/2468156
Info: http://engineering.hearsaysocial.com/hierarchical-resources-in-tastypie

Modifications:
  - ChildResource.urls() - don't skip self.override_urls() otherwise we can't provide additional urls
    and it's only a hook provided by ModelResource. It doesn't do anything by default.
  - drop in replace override_urls() with prepend_urls() due to deprecation in Tastypie v0.9.12
  - remove_api_resource_names() - use the object's actual queryset.
    Our Queryset gives uses the InheritanceManager. Without it - the way this code was - we only get
    BCContent objects back. This means new Comments are saved associated with BCContent, not the actual
    subclasses Model instance.

"""
import re

# Line changed for Django 1.3 support
from django.conf.urls import patterns, url, include
#
from django.core.urlresolvers import RegexURLPattern, RegexURLResolver

from tastypie.bundle import Bundle
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.exceptions import TastypieError, BadRequest, ApiFieldError
from tastypie.fields import RelatedField
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash


def rreplace(string, old, new, count):
    """
    Replaces a string starting from the right side
    """
    return string[::-1].replace(old[::-1], new[::-1], count)[::-1]


class CustomModelResource(ModelResource):

    def base_urls(self):
        """
        Exactly the same as ModelResource.base_urls() but removes the '/' from primary key matching
        Note: This is needed for nesting resources
        """
        return [
            url(r"^(?P<resource_name>%s)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_list'), name="api_dispatch_list"),
            url(r"^(?P<resource_name>%s)/schema%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_schema'), name="api_get_schema"),
            url(r"^(?P<resource_name>%s)/set/(?P<pk_list>\w[\w;-]*)/$" % self._meta.resource_name, self.wrap_view('get_multiple'), name="api_get_multiple"),
                url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w-]*)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
            ]


class ChildResource(CustomModelResource):
    """
    A Tastypie resource that support hierarchy.
    To use, just have your Resource inherit from ChildResource and set the parent attribute in the Meta class to a RelatedField in your Resource. The RelatedField resource must be a CustomModelResource.
    """

    class Meta:
        parent = ""  # Should be overwritten with name of the RelatedField you want to be nested under

    def __init__(self, *args, **kwargs):
        super(ChildResource, self).__init__(*args, **kwargs)

        # Set the parent resource and name
        self.parent_field_name = self._meta.parent
        self.parent_resource = None
        for field, field_type in self.fields.iteritems():
            if field == self.parent_field_name and isinstance(field_type, RelatedField):
                self.parent_resource = field_type.to
        if self.parent_resource is None:
            raise ApiFieldError("Could not find parent resource: %s" % self._meta.parent)
        self.parent_resource_instance = self.parent_resource()  # cache an instance of the parent resource

        # Add filtering for the parent
        filters_for_parent = self._meta.filtering.setdefault(self.parent_field_name, [])
        if filters_for_parent not in (ALL, ALL_WITH_RELATIONS) and "exact" not in filters_for_parent:
            if isinstance(filters_for_parent, list):
                filters_for_parent.append("exact")
            elif isinstance(filters_for_parent, tuple):
                filters_for_parent = list(filters_for_parent)
                filters_for_parent.append("exact")
                self._meta.filtering[self.parent_field_name] = tuple(filters_for_parent)

    def base_urls(self):
        # Overriding default base_urls() since we want this resource to only be accessed via the parent resource
        return []

    @property
    def urls(self):
        # need to override the urls() property b/c we need to include original urls under the parent's url
        orig_urls = super(ChildResource, self).base_urls() + self.prepend_urls()
        orig_urlpatterns = patterns("",
                                    *orig_urls
                                    )

        # Get the parent's urlpatterns to build regex for this child's urlpatterns
        # Need to munge regexes b/c using django's include with the same named parameter won't work
        # Note: the type of each element in urlpatterns could be either a RegexURLPattern or RegexURLResolver
        parent_urlpatterns = self.parent_resource_instance.urls
        parent_regexes = [p for p in parent_urlpatterns if (isinstance(p, RegexURLPattern) and p.name == "api_dispatch_detail") or (isinstance(p, RegexURLResolver))]
        if not parent_regexes:
            raise TastypieError("No parent regexes found for resource: %s" % self.__class_.name)
        if len(parent_regexes) > 1:
            raise TastypieError("Too many parent regexes found for resource: %s" % self.__class__.name)

        # Get the parent_regex based on the type
        parent_regex = parent_regexes[0]
        if isinstance(parent_regex, RegexURLPattern):
            parent_regex = parent_regex.regex.pattern
        elif isinstance(parent_regex, RegexURLResolver):
            # See RegexURLResolver._populate()'s usage of reverse_dict
            matches, pattern, defaults = parent_regex.reverse_dict["api_dispatch_detail"]
            parent_regex = pattern
        else:
            raise TastypieError("Consistency error with hierarchical urls")

        # Munge the parent regex so it correctly supports multiple levels of hierarchy
        parent_regex = parent_regex.rstrip("$")
        # Remove all of the parent resource names/pks since they could be at the beginning
        parent_regex = parent_regex.replace("(?P<parent_resource_name>", "(?P<resource_name>").replace("(?P<parent_pk>", "(?P<pk>")
        # Replace the resource name/pk with parent name/pk
        parent_regex = rreplace(parent_regex, "(?P<resource_name>", "(?P<parent_resource_name>", 1)
        parent_regex = rreplace(parent_regex, "(?P<pk>", "(?P<parent_pk>", 1)
        # Remove the remaing resource name/pk regex groupings
        # Excuse the running of regexes on regexes *sigh*
        parent_regex = re.sub("\(\?\P\<resource_name\>(.*?)\)", "\g<1>", parent_regex)
        parent_regex = re.sub("\(\?\P\<pk\>(.*?)\)", "\g<1>", parent_regex)

        urlpatterns = patterns("",
                               (parent_regex, include(orig_urlpatterns))
                               )
        return urlpatterns

    def detail_uri_kwargs(self, bundle_or_obj):
        """Sets the parent_resource_name and the parent_pk so reverse() can generate the url"""

        kwargs = super(ChildResource, self).detail_uri_kwargs(bundle_or_obj)
        obj = bundle_or_obj.obj if isinstance(bundle_or_obj, Bundle) else bundle_or_obj

        kwargs['parent_pk'] = getattr(obj, self.parent_field_name).pk
        kwargs['parent_resource_name'] = self.parent_resource._meta.resource_name

        return kwargs

    def remove_api_resource_names(self, url_dict):
        """
        Also need to remove parent_resource_name and parent_pk
        """
        kwargs_subset = super(ChildResource, self).remove_api_resource_names(url_dict.copy())

        # Added parent resource as a kwarg to filter and POST
        if "parent_resource_name" in kwargs_subset and "parent_pk" in kwargs_subset:
            kwargs_subset[self.parent_field_name] = self.parent_resource._meta.queryset.get(pk=kwargs_subset["parent_pk"])

        for key in ['parent_resource_name', 'parent_pk']:
            try:
                del(kwargs_subset[key])
            except KeyError:
                pass

        return kwargs_subset

    def alter_deserialized_list_data(self, request, data):
        if self.parent_field_name in data:
            raise BadRequest("Error: parent resource cannot be specified in the body")
        return super(ChildResource, self).alter_deserialized_list_data(request, data)

    def alter_deserialized_detail_data(self, request, data):
        if self.parent_field_name in data:
            raise BadRequest("Error: parent resource cannot be specified in the body")
        return super(ChildResource, self).alter_deserialized_detail_data(request, data)
