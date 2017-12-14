from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.dataselector, name='dataselector'),
    url(r'^site/$', views.site_choice, name = 'site_choice'),
]
