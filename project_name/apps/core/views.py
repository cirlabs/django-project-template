import json
import logging

from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.views.generic import ListView
from django.template import RequestContext

from armstrong.core.arm_layout.utils import render_model

from cir.bc_content.mixins import FilterMixin
from cir.page_layout.views import BasePageLayoutMixin


def csrf_failure(request, reason=""):
    try:
        logging.warning('CSRF FAILURE: %s From: %s'
            % (reason, request.META.get('HTTP_X_FORWARDED_FOR', 'unknown')))
    except:
        pass

    context = {'reason': reason}

    if request.is_ajax():
        return HttpResponseForbidden(
                    content=json.dumps(context),
                    content_type='application/json'
                )

    return render(request, 'base/csrf_failure.html', context, status=403)


class AjaxablePageableObjectListView(BasePageLayoutMixin, FilterMixin, ListView):
    """
    Returns an Object and a list for that object on normal and AJAX requests

    The normal ListView is designed to take a Model class and return the items
    from either that Model's default manager or a more specific Queryset. This
    view has a hybrid purpose - it returns a single Model instance like DetailView
    but it's paginatable over a list belonging to that instance like ListView.
    It also handles a standard set of GET filter params on the list.

    It's designed to be tied into BCContent's ContentQuerySetLoader so it
    can filter the list by content types and/or managers to use.

    It's also tied into ArmLayout's render_model system and returns a 'list'
    render directly when called via AJAX. On a normal HTTP request, it'll
    go through the whole ListView process to find a template, build the
    context and render the response. On AJAX, it shortcuts and just returns
    the 'list' render for the object using optional filters.

    Finally on a normal HTTP request it uses the PageLayout system to
    return the appropriate page for the Object and sets context variables
    used to juggle the page objects and template overrides.

    """
    list_render_template = 'list'
    context_object_name = "object_items"
    paginate_by = 10

    def get_content_loader(self):
        """A callable that returns a Queryset"""
        return self.object.published_by_model

    # AJAX view
    def ajax_render_to_response(self, context, **response_kwargs):
        """Only the 'list' render for this Object"""

        if not context[self.context_object_name]:
            return HttpResponse(status=204)  # No Content

        data = render_model(self.object, self.list_render_template, context, RequestContext(self.request))
        return HttpResponse(data, **response_kwargs)

    def dispatch(self, request, *args, **kwargs):
        """Override the render method for AJAX requests"""

        if request.is_ajax():
            self.render_to_response = self.ajax_render_to_response
            self.get_context_data = super(BasePageLayoutMixin, self).get_context_data  # skip PageLayout stuff

        return super(AjaxablePageableObjectListView, self).dispatch(request, *args, **kwargs)
