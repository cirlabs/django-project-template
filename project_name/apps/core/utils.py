def get_current_protocol(request):
    return 'https:' if request.is_secure() else 'http:'


def fully_qualify_if_url(request, url):
    url = "%s" % url  # cast to string for safety
    protocol = get_current_protocol(request) if url.startswith("//") else ''
    return "%s%s" % (protocol, url)
