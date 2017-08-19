from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    url(r'^repos/$', views.repos, name='webapp_repos'),
    url(r'^$', views.home, name='webapp_home'),
]
