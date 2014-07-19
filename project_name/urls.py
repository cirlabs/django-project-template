from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    # Admin
    (r'^admin/', admin.site.urls),

    # Project URLs go here
    url(r'^$', TemplateView.as_view(template_name='base.html'), name='base'),

)