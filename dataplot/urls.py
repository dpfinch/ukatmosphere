from django.conf.urls import url

from . import views
from . import dashapp

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^analysis/$', views.analysis, name='analysis'),
    url(r'^site/$', views.site_choice, name = 'site_choice'),
    url(r'^dataplot/_dash', views.dash_ajax),
    url(r'^', views.dash),
]
