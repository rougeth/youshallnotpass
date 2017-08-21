from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^setup/(?P<github_id>[\d]+)/$', views.setup_hook, name='hook_setup'),
    url(r'^pullrequest$', views.hook_pullrequest, name='hook_pullrequest'),
]
