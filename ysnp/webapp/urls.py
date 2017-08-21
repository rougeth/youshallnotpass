from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^repos/$', views.repos, name='webapp_repos'),
    url(r'^$', views.home, name='webapp_home'),
]
