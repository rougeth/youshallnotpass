from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    url(r'^setup/(?P<username>[\w\d\_\-\.]+)/(?P<repo>[\w\d\_\-\.]+)/$',
        views.setup_hook, name='hook_setup'),
    url(r'^pullrequest$', views.hook_pullrequest, name='hook_pullrequest'),
]
