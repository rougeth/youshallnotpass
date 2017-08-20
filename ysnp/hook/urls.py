from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    url(r'^setup/(?P<hash>[\w\d]{8})/$', views.setup_hook, name='hook_setup'),
    url(r'^pullrequest$', views.hook_pullrequest, name='hook_pullrequest'),
]
