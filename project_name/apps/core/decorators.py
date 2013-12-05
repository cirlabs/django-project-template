import json
from functools import wraps

from django.http import HttpResponse, HttpResponseBadRequest


def login_required_silent(view_func=None):
    """
    Decorator for views that checks that the user is logged in
    and fails with a 400 if they aren't. Good for AJAX requests
    that require a user.

    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated():
                return HttpResponseBadRequest("Not logged in.")
            return view_func(request, *args, **kwargs)
        return wrapper

    return decorator if not view_func else decorator(view_func)


def simple_json_response(view_func=None):
    """
    Decorator for AJAX views.
    Return success/error response based on [True|None]/False return value
    from decorated function.

    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            result = view_func(*args, **kwargs)
            if result is False:
                status = "error"
                response = HttpResponseBadRequest
            else:
                status = "success"
                response = HttpResponse
            return response(
                content=json.dumps(dict(status=status)),
                content_type='application/json'
            )
        return wrapper

    return decorator if not view_func else decorator(view_func)
