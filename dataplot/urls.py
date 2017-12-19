from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^analysis/$', views.analysis, name='analysis'),
    url(r'^site/$', views.site_choice, name = 'site_choice'),
]
