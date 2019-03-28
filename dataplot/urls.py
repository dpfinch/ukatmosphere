from django.conf.urls import url

from . import views
from . import dashapp # this loads the Dash app
from django.urls import re_path

urlpatterns = [
    re_path(r'^$', views.homepage, name='homepage'),
    re_path(r'^about/$', views.about, name='about'),
    # url(r'^analysis/$', views.analysis, name='analysis'),
    # url(r'^site/$', views.site_choice, name = 'site_choice'),
    re_path(r'^dataplot/_dash-', views.dash_json),
    re_path(r'^dataplot/assets/', views.dash_guess_mimetype),
    re_path(r'^dataplot/', views.dash_index),
    # re_path('^', views.dash_index),
]
