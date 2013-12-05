from django.contrib.sites.models import get_current_site


def current_site(request):
    """Returns Site or RequestSite if the Sites framework isn't installed"""
    return dict(CURRENT_SITE=get_current_site(request))
