from django.conf import settings
from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.views.static import serve as static_serve
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    # Simple login for securing site on Heroku
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}),

    # Admin
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', admin.site.urls),

    # Project URLs go here
    (r'^$', TemplateView.as_view(template_name='index.html')),

)